FROM apache/airflow:2.6.3

WORKDIR /app/batch/

COPY ./requirements.txt /app/batch
COPY . /app/batch

RUN pip install --no-cache-dir -r requirements.txt

CMD ["webserver", "--port", "8080"]