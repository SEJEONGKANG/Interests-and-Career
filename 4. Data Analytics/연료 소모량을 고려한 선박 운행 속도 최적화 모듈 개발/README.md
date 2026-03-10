# 부산항 접안 시뮬레이터

SNU SCM × KRISO 외주 용역 산출물

> 실제 부산항 해역 기반 / 풍향·풍속 영향 반영 / 강화학습 기반 항로 최적화 엔진

---

## 데모 서비스

**http://www.scm-kriso.cloud/**

---

## 사용자 화면

### ▶ 메인 화면

<img src="./app/static/infer/sample_main.png">

### ▶ 최적 항로 시각화 및 ETA·배출량·비용 상세 결과

<img src="./app/static/infer/sample_results.png">

---

## 소개

본 프로젝트는 **부산항 주변 해상 격자 환경**에서  
풍속·풍향·지형·ECA/VSR 규제·연료비용·탄소배출 등을 고려하여  
**강화학습 기반 최적 항로를 추천하는 시스템**입니다.

- 웹 프론트엔드: Leaflet 기반 지도 UI
- 백엔드: Flask
- 시뮬레이션 엔진: 커스텀 강화학습 환경(`environment.py`)
- 정책 추론: `main_inference.py`

---

## 기능 요약

### 지도 기반 시뮬레이션

- 지도를 클릭하여 시작 위치 선택
- 출발 시간과 기상청 API 기반 실시간 바람 정보 입력
- Drift·육지 충돌 회피 로직 적용
- 실제 지형 기반 ECA/VSRZ Overlay 표시

### 강회학습 기반 항로 계획

- Action: 8방향 × 속력
- 해상 풍향에 의한 불확실성 고려
- 육지 충돌 방지 자동 회피
- ETA 목적 시점 준수 및 연료·탄소 비용 최적화

### 시각화 및 분석

- 항로 polyline 표시
- 각 Segment를 속도에 따라 색상 시각화
- ETA 경과 시간 Tooltip
- CO₂·SOx 배출량, 비용 요약

### API

- /docs (Swagger UI) 및 test_api.py에서 테스트 가능
- /api/info 서비스 메타데이터 및 엔드포인트 목록 반환 기능
- /api/health 상태 정보 반환 기능(모델/설정/데이터 소스 상태 포함)
- /api/wind 풍향/풍속 및 데이터 소스 반환 기능
- /api/guidance 접안 가이던스 생성 기능

---

## Docker 실행

### 1. docker compose 사용

```bash
# 이미지 빌드 + 컨테이너 실행
docker compose up --build -d
```

- 브라우저 접속
- KMA_API_KEY는 docker-compose.yml의 environment 또는 .env 파일에서 설정

### 2. docker run 으로 직접 실행

```bash
# 이미지 빌드
docker build -t scm-kriso .

# 컨테이너 실행 (호스트 80 → 컨테이너 8000)
docker run -d \
  --name scm-kriso \
  -p 80:8000 \
  -e KMA_API_KEY=여기에_기상청_API_키_입력 \
  scm-kriso
```
