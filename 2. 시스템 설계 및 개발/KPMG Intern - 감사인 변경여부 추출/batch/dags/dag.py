from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from main import run

# DAG 설정
default_args = {
    'owner': 'airflow',
    'depends_on_past': True,
    'start_date': datetime(2023, 8, 27),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(dag_id='data_push_dag',
         default_args=default_args,
         description='XML 원문 처리 및 결과 적재를 위한 DAG',
         schedule_interval=timedelta(days=1),
         catchup=False,
         ) as dag:

    push_data_task = PythonOperator(
        task_id='push_data_to_mysql_task',
        python_callable=run,
    )

    push_data_task  # 작업 간의 의존성