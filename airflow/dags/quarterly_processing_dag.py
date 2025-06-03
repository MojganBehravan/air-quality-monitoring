from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='quarterly_processing_dag',
    default_args=default_args,
    description='Processes pollution data quarterly using Spark',
    schedule_interval='@quarterly',  # Runs Jan, Apr, Jul, Oct
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['processing'],
) as dag:

    spark_process = DockerOperator(
        task_id='run_spark_processing',
        image='air-quality/processing',
        container_name='airflow_processing',
        api_version='auto',
        auto_remove=True,
        command='spark-submit --master local /app/process.py',
        docker_url='unix://var/run/docker.sock',
        network_mode='air-quality-monitoring_default',
        mount_tmp_dir=False,
        mounts=[
            Mount(source='/var/run/docker.sock', target='/var/run/docker.sock', type='bind'),
            Mount(source='/opt/airflow/processing', target='/app', type='bind'),
            Mount(source='/opt/airflow/data', target='/data', type='bind'),
        ],
    )
