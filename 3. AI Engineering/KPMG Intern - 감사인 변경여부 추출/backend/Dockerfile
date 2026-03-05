# FastAPI 애플리케이션을 위한 베이스 이미지 선택
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

WORKDIR /app/backend

COPY ./requirements.txt /app/backend
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/backend

# FastAPI 서버를 실행
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]