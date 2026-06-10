# API 명세서

## 1. GET `/api/health`

서버 상태 확인용입니다.

```json
{
  "status": "ok"
}
```

## 2. GET `/api/departments`

학과 선택 화면에 필요한 학과 기준 데이터를 반환합니다.

```json
{
  "departments": [
    {
      "id": 1,
      "department": "문과/사회과학",
      "mainUsage": "문서작성,강의수강,자료조사,발표",
      "recommendedCpu": "i5/Ryzen5 이상",
      "minRamGb": 16,
      "minStorageGb": 512,
      "recommendedGpu": "내장 그래픽 가능",
      "avgBudgetKrw": 1200000,
      "valueBudgetKrw": 900000
    }
  ]
}
```

## 3. GET `/api/laptops`

전체 노트북 후보 45개를 반환합니다.

## 4. POST `/api/recommend`

React 화면에서 입력한 회원 정보와 추천 조건을 백엔드로 전송합니다.

### Request

```json
{
  "member": {
    "name": "이은아",
    "studentId": "20261234",
    "grade": "3학년"
  },
  "department": "컴퓨터공학/AI",
  "budget": 1800000,
  "priorities": ["price", "performance"],
  "os": "windows",
  "canInstallWindows": true,
  "limit": 5
}
```

### Response

```json
{
  "member": {
    "name": "이은아",
    "studentId": "20261234",
    "grade": "3학년"
  },
  "departmentSpec": {},
  "requestSummary": {},
  "recommendations": [
    {
      "rank": 1,
      "brand": "Lenovo",
      "model": "ThinkPad E16",
      "score": 184,
      "priceLabel": "120~180만원",
      "imagePath": "/laptops/09_lenovo-thinkpad-e16.png",
      "reasons": ["학과 권장 CPU 충족", "RAM 16GB로 권장 기준 충족"]
    }
  ],
  "notice": []
}
```

## 백엔드 변경 방향

기존 구조는 `input()`으로 값을 받고 `recommend_result.txt`로 결과를 저장하는 CLI 방식이었습니다. 이번 구조에서는 입력값을 JSON으로 받고, 추천 결과를 JSON 응답으로 반환합니다. 따라서 React 화면에서는 추천 결과를 카드, 비교표, 상세 근거로 바로 렌더링할 수 있습니다.
