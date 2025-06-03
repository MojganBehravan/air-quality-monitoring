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
    dag_id='monthly_ingestion_dag',
    default_args=default_args,
    description='Ingests new monthly pollution files to HDFS',
    schedule_interval='@monthly', 
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['ingestion'],
) as dag:

        ingest_new_files = DockerOperator(
        task_id='run_ingestion_script',
        image='air-quality/ingestion',
        container_name='airflow_ingestion',
        api_version='auto',
        auto_remove=True,
        command='python ingest.py',
        docker_url='unix://var/run/docker.sock',
        network_mode='air-quality-monitoring_default',
        mount_tmp_dir=False,
        mounts=[
            Mount(source='/var/run/docker.sock', target='/var/run/docker.sock', type='bind'),
            Mount(source='/opt/airflow/data', target='/data', type='bind'),
            Mount(source='/opt/airflow/ingestion', target='/app', type='bind'),
        ],
    )
