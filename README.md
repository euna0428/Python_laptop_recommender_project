# 학과별 노트북 추천 웹 서비스

학과, 예산, 운영체제, 우선순위를 입력하면 조건에 맞는 노트북을 추천하는 웹 서비스입니다. 기존 `recommend_laptop.py` 기반 추천 로직을 유지하면서, 현재 프로젝트는 **React 프론트엔드 + FastAPI 백엔드 + CSV 데이터** 구조로 확장되어 있습니다.

---

## 1. 프로젝트 핵심 요약

| 구분 | 내용 |
|---|---|
| 프로젝트명 | 학과별 노트북 추천 웹 서비스 |
| 목적 | 사용자의 학과와 예산에 맞는 노트북 추천 |
| 추천 결과 | TOP 5 노트북, BEST PICK, 추천 점수, 추천 이유, 비교표 |
| 프론트엔드 | React JS, Vite, Framer Motion |
| 백엔드 | Python, FastAPI, Pandas |
| 데이터 방식 | CSV 기반 데이터 관리 |
| 실행 방식 | 백엔드와 프론트엔드 서버를 각각 실행 |

---

## 2. 현재 구현된 기능

- 회원 이름, 학번 또는 구분값, 학년 입력
- 학과별 권장 스펙 기준 추천
- 예산 범위 반영
- 가격, 성능, 휴대성 우선순위 반영
- Windows, macOS, FreeDOS, 상관없음 OS 조건 반영
- Windows 직접 설치 가능 여부 반영
- 추천 노트북 TOP 5 출력
- BEST PICK 강조 표시
- 노트북 이미지 매칭 출력
- 추천 이유와 점수 표시
- 추천 결과 비교표 제공
- React 기반 네온형 UI 적용
- 커스텀 마우스 커서 효과 적용

---

## 3. 최종 프로젝트 구조

```text
laptop_recommender_project_v4
├─ backend
│  ├─ app
│  │  ├─ main.py
│  │  └─ recommender.py
│  ├─ data
│  │  ├─ department_specs.csv
│  │  ├─ laptop_candidates.csv
│  │  ├─ laptop_image_mapping.csv
│  │  └─ price_sources.csv
│  └─ requirements.txt
│
├─ frontend
│  ├─ public
│  │  └─ laptops
│  ├─ src
│  │  ├─ api
│  │  ├─ components
│  │  ├─ utils
│  │  ├─ App.jsx
│  │  ├─ main.jsx
│  │  └─ styles.css
│  ├─ index.html
│  ├─ package.json
│  └─ vite.config.js
│
├─ docs
├─ department_specs.csv
├─ laptop_candidates.csv
├─ price_sources.csv
├─ recommend_laptop.py
├─ recommend_result.txt
├─ start_backend.bat
├─ start_frontend.bat
└─ README.md
```

---

## 4. 실행 전 필수 확인

### Python

백엔드는 **Python 3.12** 기준으로 실행하는 것을 권장합니다.

```powershell
python -V
```

Python 3.14 환경에서는 `pandas==2.2.3` 설치 과정에서 오류가 발생할 수 있으므로, Python 3.12 가상환경을 사용합니다.

### Node.js / npm

프론트엔드는 Node.js와 npm이 필요합니다.

```powershell
node -v
npm -v
```

버전이 출력되면 프론트엔드 실행이 가능합니다.

---

## 5. 실행 순서

### 1단계. 백엔드 실행

```powershell
cd C:\laptop_recommender_project_v4
py -3.12 -m venv .venv
.venv\Scripts\activate
cd backend
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

백엔드 확인 주소:

```text
http://127.0.0.1:8000/api/health
```

정상 응답:

```json
{"status":"ok"}
```

### 2단계. 프론트엔드 실행

백엔드 서버를 켠 상태에서 새 터미널을 열고 실행합니다.

```powershell
cd C:\laptop_recommender_project_v4\frontend
npm install --no-audit --no-fund
npm run dev
```

프론트엔드 접속 주소:

```text
http://127.0.0.1:5173
```

---

## 6. 서버 실행 상태 기준

| 서버 | 주소 | 상태 |
|---|---|---|
| 백엔드 | `http://127.0.0.1:8000` | FastAPI 서버 |
| 프론트엔드 | `http://127.0.0.1:5173` | React 화면 |

정상 실행을 위해서는 **두 서버가 모두 켜져 있어야 합니다.**

---

## 7. 데이터 관리 기준

웹 서비스에서 실제로 사용하는 데이터는 `backend/data` 폴더 안의 파일입니다.

| 파일 | 역할 |
|---|---|
| `department_specs.csv` | 학과별 권장 CPU, RAM, 저장공간, GPU, 예산 기준 |
| `laptop_candidates.csv` | 추천 후보 노트북 45개 데이터 |
| `price_sources.csv` | 가격 범위 산정 참고 데이터 |
| `laptop_image_mapping.csv` | 노트북 모델과 이미지 파일 매칭 데이터 |

루트 경로의 CSV 파일은 기존 CLI 프로그램 유지용입니다. 웹 화면에 반영하려면 `backend/data` 안의 CSV를 수정해야 합니다.

---

## 8. 추천 로직 기준

추천 점수는 다음 기준을 조합해 계산합니다.

| 기준 | 반영 내용 |
|---|---|
| 학과 스펙 | CPU, RAM, 저장공간, GPU 기준 충족 여부 |
| 예산 | 사용자 예산과 예상 구매가 범위 비교 |
| 성능 | CPU 점수, GPU 점수, RAM 여유 여부 |
| 휴대성 | 학과별 선호 무게와 최대 허용 무게 비교 |
| 운영체제 | Windows, macOS, FreeDOS 조건 반영 |
| 학과 태그 | 학과와 적합 태그가 일치하는 후보 우선 추천 |

추천 결과는 점수순으로 정렬되며, 상위 5개 노트북이 화면에 출력됩니다.

---

## 9. API 구성

| 메서드 | 경로 | 기능 |
|---|---|---|
| GET | `/api/health` | 백엔드 서버 상태 확인 |
| GET | `/api/departments` | 학과 목록과 권장 스펙 조회 |
| GET | `/api/laptops` | 전체 노트북 후보 조회 |
| POST | `/api/recommend` | 사용자 조건 기반 TOP 5 추천 결과 반환 |

---

## 10. 주요 파일 역할

### 프론트엔드

| 파일 | 역할 |
|---|---|
| `frontend/src/App.jsx` | 화면 전환, API 호출, 상태 관리 |
| `frontend/src/components/IntroSection.jsx` | 메인 인트로 화면 |
| `frontend/src/components/Wizard.jsx` | 회원 정보와 추천 조건 입력 화면 |
| `frontend/src/components/Results.jsx` | 추천 결과 출력 화면 |
| `frontend/src/components/CursorGlow.jsx` | 커스텀 마우스 커서 효과 |
| `frontend/src/styles.css` | 전체 UI, 반응형, 애니메이션 스타일 |
| `frontend/src/api/client.js` | 백엔드 API 요청 함수 |

### 백엔드

| 파일 | 역할 |
|---|---|
| `backend/app/main.py` | FastAPI 앱, API 라우터 정의 |
| `backend/app/recommender.py` | CSV 로드, 필터링, 추천 점수 계산 |
| `backend/requirements.txt` | 백엔드 패키지 목록 |

---

## 11. 기존 CLI 실행

기존 Python 터미널 프로그램도 유지되어 있습니다.

```powershell
cd C:\laptop_recommender_project_v4
python recommend_laptop.py
```

실행 결과는 `recommend_result.txt`에 저장됩니다.

---

## 12. 자주 발생하는 문제

### 백엔드 연결 실패

프론트 화면에 백엔드 연결 오류가 뜨면 백엔드 서버가 꺼져 있는 상태입니다.

확인 주소:

```text
http://127.0.0.1:8000/api/health
```

해결:

```powershell
cd C:\laptop_recommender_project_v4\backend
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### npm 명령어 인식 실패

`node -v`, `npm -v`가 실행되지 않으면 Node.js 설치 후 PowerShell 또는 PyCharm을 다시 실행합니다.

### npm install 오류

설치 중 오류가 발생하면 아래 명령어를 실행합니다.

```powershell
cd C:\laptop_recommender_project_v4\frontend
Remove-Item -Recurse -Force node_modules -ErrorAction SilentlyContinue
Remove-Item -Force package-lock.json -ErrorAction SilentlyContinue
npm cache clean --force
npm install --no-audit --no-fund
```

### pandas 설치 실패

Python 3.14 환경에서 발생할 수 있습니다. Python 3.12 설치 후 `.venv`를 삭제하고 다시 생성합니다.

```powershell
cd C:\laptop_recommender_project_v4
deactivate
Remove-Item -Recurse -Force .venv
py -3.12 -m venv .venv
.venv\Scripts\activate
```

---

## 13. 구매 전 확인 사항

추천 결과의 링크는 직접 구매 링크가 아니라, 추천 스펙과 일치하는 모델을 찾기 위한 검색 링크입니다. 실제 구매 전 아래 항목을 확인해야 합니다.

- RAM 용량
- SSD 용량
- GPU 모델
- Windows 포함 여부
- FreeDOS 여부
- 무게와 화면 크기
- 가격 변동 여부

---

## 14. 현재 개발 상태

- Python CLI 추천 로직 유지
- FastAPI 백엔드 구성 완료
- React 프론트엔드 구성 완료
- 메인 화면 UI 수정 완료
- 공통 헤더 제거 반영
- 커스텀 마우스 커서 적용
- 노트북 이미지 매칭 적용
- 추천 결과 카드 UI 적용

