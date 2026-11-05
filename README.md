# 학과별 맞춤형 노트북 추천 시스템

학과, 예산, 운영체제, 우선순위를 입력하면 조건에 맞는 노트북 TOP 5를 점수와 선정 사유와 함께 추천하는 웹 서비스입니다.

## 작업 정보

| 구분 | 내용 |
|---|---|
| 작업 기간 | 2026.03.09 ~ 2026.06.08 |
| 작업 인원 | 단독 개발(2인 팀) |
| 내 역할 | 기획·총괄, 추천 알고리즘, 데이터 구축, 프론트·백엔드 개발 (ChatGPT 협업) |
| 작업 툴 | Python, FastAPI, Pandas, React(Vite), Node.js, HTML |

## 작품 소개

학과마다 필요한 사양이 다르다는 점에서 출발해, 학과별 권장 사양과 예산·성능·휴대성 선호를 반영한 추천 서비스를 만들었습니다. Python CLI 프로그램으로 시작해 **React·FastAPI 웹 서비스로 전환**했습니다.

## 내가 한 일

- **데이터 구축**: 학과별 사용 목적과 권장 사양을 조사해 **8개 학과 기준표**(CPU·RAM·SSD·GPU·예산·휴대성)를 작성하고, 다나와·TrendForce 등 **가격·시장 자료 7건**을 바탕으로 **45개 제품 데이터**를 직접 구성했습니다.
- **추천 알고리즘**: 학과 스펙 충족 여부, 예산 범위, 성능(CPU·GPU·RAM), 휴대성, 운영체제, 학과 태그를 결합한 가중치 점수화로 TOP 5를 산출합니다.
- **백엔드**: FastAPI REST API 4종을 만들고 Pydantic으로 입력을 검증했습니다. pandas로 읽는 CSV 조회에는 `lru_cache`를 적용했습니다.
- **프론트엔드**: React 5단계 설문과 추천 카드 UI, 추천 결과 비교표를 구현했습니다.

## 개발 과정

- 처음에는 터미널에서 학과와 예산을 입력하면 결과를 파일로 저장하는 Python 프로그램이었습니다.
- 웹으로 옮길 때 ChatGPT에 "기존 점수 계산은 변경하지 않는다"는 조건을 먼저 주고, 추천 함수는 그대로 둔 채 FastAPI 요청 처리와 React 입력 화면을 나눴습니다.
- CLI와 웹 백엔드가 읽는 CSV 위치가 달라 데이터 경로와 컬럼 연결을 따로 점검했습니다.
- 추천 규칙은 범주 조합 7,227건으로 검사했고, 학과별 대표 시나리오 24건(추천 결과 120행)의 점수 합계·정렬·반환 개수·선정 이유를 확인했습니다.

## 결과

- 정상 요청 시 추천 5건과 **점수·선정 사유**를 반환해 추천 근거를 확인할 수 있습니다.
- 잘못된 요청 값은 Pydantic 검증으로 422, 존재하지 않는 학과는 404로 응답하는 것을 확인했습니다.

| 메서드 | 경로 | 기능 |
|---|---|---|
| GET | `/api/health` | 서버 상태 확인 |
| GET | `/api/departments` | 학과 목록·권장 스펙 조회 |
| GET | `/api/laptops` | 노트북 후보 조회 |
| POST | `/api/recommend` | 조건 기반 TOP 5 추천 |

## 한계

- 후보 노트북 45개는 직접 구성한 데이터라 시장 전체를 대표하지 않습니다.
- 가격은 조사 시점 기준 참고값이며, 구매 전 가격 변동 확인이 필요합니다.

## 폴더 구조

```text
backend/    FastAPI 앱, backend/data (웹에서 쓰는 CSV)
frontend/   React(Vite) 화면
docs/       API_CONTRACT.md, IMPLEMENTATION_NOTES.md
```

## 실행 방법

백엔드와 프론트엔드를 각각 실행합니다. 설치·실행 순서와 자주 발생하는 문제는 [상세 개발 기록](https://github.com/euna0428/python_laptop_recommender_project/blob/main/docs/DEV_README.md)에 정리했습니다.

## 관련 문서

- [API 명세](https://github.com/euna0428/python_laptop_recommender_project/blob/main/docs/API_CONTRACT.md)
- [구현 노트](https://github.com/euna0428/python_laptop_recommender_project/blob/main/docs/IMPLEMENTATION_NOTES.md)
- [상세 개발 기록](https://github.com/euna0428/python_laptop_recommender_project/blob/main/docs/DEV_README.md)
- [학과별 추천 결과 이미지](https://github.com/euna0428/python_laptop_recommender_project/tree/main/docs/images)
- [검증 데이터 폴더](https://github.com/euna0428/python_laptop_recommender_project/tree/main/docs/%EA%B2%80%EC%A6%9D_%EB%8D%B0%EC%9D%B4%ED%84%B0)
- [학과별 24건 검증 결과](https://github.com/euna0428/python_laptop_recommender_project/blob/main/docs/%EA%B2%80%EC%A6%9D_%EB%8D%B0%EC%9D%B4%ED%84%B0/%ED%95%99%EA%B3%BC%EB%B3%84_24%EA%B1%B4_%EA%B2%80%EC%A6%9D%EA%B2%B0%EA%B3%BC.csv)
- [학과별 추천 TOP5 120행](https://github.com/euna0428/python_laptop_recommender_project/blob/main/docs/%EA%B2%80%EC%A6%9D_%EB%8D%B0%EC%9D%B4%ED%84%B0/%ED%95%99%EA%B3%BC%EB%B3%84_%EC%B6%94%EC%B2%9C_TOP5_120%ED%96%89.csv)
- [기존 README](https://github.com/euna0428/python_laptop_recommender_project/blob/main/README_PREVIOUS.md)
