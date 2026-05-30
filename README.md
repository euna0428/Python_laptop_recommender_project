# 학과별 노트북 추천 프로그램 v4

## 변경 목적
이 버전은 기존의 `참고 가격대`를 임의 단일 가격으로 보여주던 문제를 수정했습니다.
이제 가격은 `예상 구매가 범위`로 표시하고, 링크는 추천 스펙과 맞는 옵션 검색어를 포함한 다나와 검색 링크로 제공합니다.

## 핵심 변경 사항

1. 가격 기준 변경
   - 기존: `price_krw` 단일 가격
   - 변경: `expected_price_min_krw`, `expected_price_max_krw`
   - 의미: 실시간 최저가가 아니라 2026년 메모리/SSD 가격 상승과 국내 가격비교 검색 결과를 반영한 예상 구매가 범위

2. 링크 기준 변경
   - 기존: 모델명 중심 네이버쇼핑 검색 링크
   - 변경: 브랜드 + 모델명 + CPU + RAM + 저장공간 + GPU + OS 조건이 들어간 다나와 검색 링크
   - 예: `Lenovo LOQ 15 RTX4060 i7 16GB 512GB RTX4060 FreeDOS 노트북`

3. 저장공간 표기 변경
   - 1024GB → 1TB

4. 설문 항목 보강
   - 학과 선택
   - 예산 입력
   - 가격/성능/휴대성 다중 선택
   - 운영체제 선택
   - Windows 직접 설치 가능 여부

5. 구매 전 확인 문구 추가
   - RAM/SSD/GPU/OS 옵션 확인
   - FreeDOS 여부 확인
   - 검색 결과에 다른 옵션이 섞일 수 있음 안내

## 실행 방법

```bash
python recommend_laptop.py
```

## 파일 구성

```text
recommend_laptop.py       실행 파일
laptop_candidates.csv     노트북 후보 데이터
 department_specs.csv      학과별 권장 스펙 데이터
price_sources.csv         가격 범위 산정 참고 출처
recommend_result.txt      실행 결과 저장 파일
```

## 가격 데이터 기준

가격은 실시간 크롤링이 아닙니다. 다음 기준을 반영한 예상 구매가 범위입니다.

- 2026년 DRAM/NAND/SSD 가격 상승 이슈
- 국내 가격비교 검색 결과의 RAM/SSD/GPU 옵션별 가격 스니펫
- OS 포함 여부와 FreeDOS 여부
- RAM 16GB/32GB, SSD 512GB/1TB 옵션 차이
- RTX4050/4060/4070 등 GPU 등급 차이

## 주의

검색 링크는 모델 구매를 보장하는 직접 구매 링크가 아니라, 추천 스펙과 일치하는 옵션을 찾기 위한 검색 링크입니다. 쇼핑몰 검색 결과는 시간이 지나면 바뀔 수 있으므로, 실제 구매 전 아래 항목을 확인해야 합니다.

- RAM 용량
- SSD 용량
- GPU 모델
- Windows 포함 여부
- FreeDOS 여부
- 무게와 화면 크기
