FROM python:3.11-slim

# 빌드 도구 — 필요한 경우에만 설치
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# 컨테이너 내부 작업 디렉토리
WORKDIR /app

# 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 전체 프로젝트 복사
COPY . .

# Python 경로 설정
ENV PYTHONPATH=/app

# Flask/Gunicorn 포트
ENV PORT=8000

# Gunicorn으로 Flask 실행
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "app.app:app"]
