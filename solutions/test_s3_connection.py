from airflow import DAG
from airflow.providers.amazon.aws.operators.s3 import S3ListOperator
from datetime import datetime

with DAG(
    dag_id='test_s3_connection',
    start_date=datetime(2023, 1, 1),
    schedule="@once",
    catchup=False,
    tags=['s3', 'listing'],
) as dag:
    list_minio_bucket = S3ListOperator(
        task_id='list_minio_test_bucket',
        bucket='minio-test-bucket-1',
        aws_conn_id='s3_default',  
    )
