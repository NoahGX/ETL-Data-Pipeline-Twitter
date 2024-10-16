from airflow import DAG
from datetime import datetime, timedelta
from twitter_etl import run_twitter_etl
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    'twitter_dag',
    default_args=default_args,
    description='A simple Twitter ETL DAG',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 10, 15),
    # or "start_date=days_ago(1)" for dynamic start
    catchup=False,
)

run_etl = PythonOperator(
    task_id='run_twitter_etl',
    python_callable=run_twitter_etl,
    dag=dag, 
)

run_etl