from airflow import DAG
from airflow.providers.amazon.aws.transfers.sql_to_s3 import SqlToS3Operator
from datetime import datetime

with DAG(
    dag_id='transfer_mysql_to_s3',
    start_date=datetime(2023, 1, 1),
    schedule="@once",
    catchup=False,
    tags=['mysql', 's3', 'transfer'],
) as dag:
    transfer_loyalty_transactions = SqlToS3Operator(
        task_id='transfer_loyalty_transactions_to_s3',
        query='SELECT * FROM loyalty.transactions',  # SQL query to select data from your MySQL table
        s3_bucket='minio-test-bucket-1',  # The S3 bucket to transfer data to
        s3_key='loyalty_transactions/transactions_data.parquet',  # The S3 key (path and filename) for the output file
        sql_conn_id='mysql',  # The Airflow connection ID for your MySQL database
        aws_conn_id='s3_default',  # The Airflow connection ID for your S3 bucket
        file_format='parquet',  # Output file format (e.g., 'csv', 'json', 'parquet')
        # Optional: Set replace=True to overwrite the S3 key if it already exists.
        # If set to False (default), the task will fail if the key exists.
        replace=True,
        # Optional: compression='gzip' for gzipped output
        # compression=None,
        # Optional: field_delimiter for CSV files
        # field_delimiter=','
    )
