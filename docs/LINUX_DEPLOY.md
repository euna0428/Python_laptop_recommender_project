# 08_Linux_배포_운영점검

Vercel 배포와 별도로, 같은 서비스를 Linux(Ubuntu) 환경에 nginx와 Docker Compose로 직접 배포하고 접속 기록 확인과 재시작까지 점검한 기록이다.

## 1. 작업 개요

| 구분 | 내용 |
|---|---|
| 작업일 | 2026-11-17 |
| 목적 | 서버 관리를 대신해 주는 Vercel 없이, 서버 구성·배포·로그 확인·재시작을 직접 해 본다 |
| 실행 환경 | Windows PC의 WSL2, Ubuntu 24.04 LTS |
| 사용 도구 | Docker 29.1.3, Docker Compose v2, docker-buildx, nginx 1.27 |
| 설정 파일 | `docker-compose.yml`, `deploy/nginx.conf`, `deploy/api.Dockerfile`, `deploy/web.Dockerfile` |
| 환경 선택 이유 | 무료 클라우드 서버(Oracle Cloud) 계정을 만들지 못해, 같은 Ubuntu 환경을 PC의 WSL2에 설치해 진행했다 |

## 2. 배포 구조

| 컨테이너 | 이미지 | 하는 일 | 포트 |
|---|---|---|---|
| web | node:20-alpine에서 React 빌드 → nginx:1.27-alpine | 빌드된 화면 파일을 제공하고, `/api/` 요청은 api 컨테이너로 넘긴다 | 80 (외부 공개) |
| api | python:3.12-slim | FastAPI 서버를 uvicorn으로 실행한다 | 8000 (컨테이너끼리만 사용) |

요청 흐름은 `브라우저 → nginx(web, 80) → /api/ 요청만 FastAPI(api, 8000)` 이다.

설정에서 정한 기준은 다음과 같다.

| 항목 | 설정 | 이유 |
|---|---|---|
| API 전달 | `location /api/ { proxy_pass http://api:8000; }` | 화면과 API를 같은 주소(80)로 제공해 브라우저 CORS 설정이 필요 없게 한다 |
| 화면 새로고침 | `try_files $uri $uri/ /index.html;` | React 화면 주소에서 새로고침해도 404가 나지 않게 한다 |
| 응답 대기 | `proxy_connect_timeout 5s`, `proxy_read_timeout 30s` | API가 멈췄을 때 요청이 무한정 기다리지 않게 한다 |
| 상태 점검 | api 컨테이너가 30초마다 `/api/health` 호출, 5초 안에 응답 없으면 실패, 3번 실패 시 unhealthy | 서버가 살아 있는지 Docker가 직접 확인한다 |
| 재시작 정책 | `restart: unless-stopped` | 컨테이너가 꺼지면 다시 켜지게 한다 (직접 내린 경우 제외) |
| API 포트 | 외부에 열지 않음 | 밖에서는 nginx를 거쳐서만 API에 접근하게 한다 |

## 3. 배포 절차

```bash
# 1) Windows PowerShell(관리자)에서 Ubuntu 설치
wsl --install -d Ubuntu-24.04

# 2) Ubuntu에서 Docker 설치, 현재 사용자를 docker 그룹에 추가
sudo apt update
sudo apt install -y docker.io docker-compose-v2 docker-buildx git
sudo usermod -aG docker $USER

# 3) 내 홈 폴더에 코드 받기
cd ~
git clone https://github.com/euna0428/python_laptop_recommender_project.git
cd python_laptop_recommender_project

# 4) 이미지 빌드 후 컨테이너 2개 실행
docker compose up -d --build
```

첫 빌드는 이미지 내려받기를 포함해 67.2초 걸렸다.

## 4. 운영 점검 결과 (2026-11-17)

| 점검 | 명령 | 결과 |
|---|---|---|
| 컨테이너 상태 | `docker compose ps` | api `Up 39 seconds (healthy)`, web `Up 39 seconds`, `0.0.0.0:80->80/tcp` |
| API 상태 확인 | `curl localhost/api/health` | `{"status":"ok"}` |
| 화면 동작 | 브라우저에서 `http://localhost` 접속 후 추천 실행 | 학과 선택부터 TOP 5 결과까지 정상 표시 |
| 접속 기록 | `docker compose logs --tail 10 web` | `GET /api/departments 200`, `POST /api/recommend 200`, 노트북 이미지 5개 `200`, `GET /api/health 200` |
| API 서버만 재시작 | `docker compose restart api` → `docker compose ps` | api `Up 8 seconds (health: starting)`, web은 그대로 `Up 3 minutes` |

접속 기록 일부(사용자 에이전트 등 긴 부분은 생략):

```text
web-1 | 172.18.0.1 - - [16/Nov/2026:16:20:04 +0000] "GET /api/departments HTTP/1.1" 200 3493
web-1 | 172.18.0.1 - - [16/Nov/2026:16:20:27 +0000] "POST /api/recommend HTTP/1.1" 200 7386
web-1 | 172.18.0.1 - - [16/Nov/2026:16:21:03 +0000] "GET /api/health HTTP/1.1" 200 15 "-" "curl/8.5.0"
```

## 5. 작업 중 겪은 문제

| 문제 | 원인 | 해결 |
|---|---|---|
| PowerShell에서 `docker ps` 실행 시 `failed to connect to the docker API at npipe:////./pipe/dockerDesktopLinuxEngine` | Windows에 깔려 있던 Docker Desktop 명령이 실행됐고, Docker Desktop은 꺼져 있었다 | `wsl -d Ubuntu-24.04`로 Ubuntu에 들어가 Ubuntu 안의 Docker로 실행했다 |
| 코드가 `/mnt/c/WINDOWS/system32` 아래에 받아짐 | Ubuntu를 관리자 PowerShell에서 열어 시작 위치가 Windows 시스템 폴더였다 | 잘못 받은 폴더를 지우고 `cd ~` 후 홈 폴더에서 다시 받았다 |
| 지운 폴더 안에서 `git clone` 실패 (`could not create work tree dir`) | 현재 위치가 방금 지운 폴더였다 | `cd ~`로 위치를 옮긴 뒤 다시 실행했다 |
| `docker compose` 빌드에 buildx 필요 | Ubuntu 기본 docker.io 패키지에는 buildx가 따로 설치되지 않는다 | `docker-buildx` 패키지를 추가로 설치했다 |

## 6. 한계와 다음 단계

| 구분 | 내용 |
|---|---|
| 접속 범위 | 클라우드 서버가 아니라 PC 안의 Ubuntu라서, PC가 켜져 있을 때 이 PC에서만 접속된다 |
| 미확인 | API 재시작 뒤 `health: starting`에서 `healthy`로 바뀌는 것은 다시 확인하지 않았다 |
| 미적용 | HTTPS, 도메인 연결, 모니터링 도구, 로그 보관 기간 설정 |
| 다음 단계 | 클라우드 Linux 서버에 같은 설정으로 배포, `.dockerignore` 추가, HTTPS 적용 |
