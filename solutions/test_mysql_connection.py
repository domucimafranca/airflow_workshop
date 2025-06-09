from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.operators.python import PythonOperator
from airflow.decorators import dag, task
from datetime import datetime

def _query_data(conn_id):
    hook = MySqlHook(mysql_conn_id=conn_id)
    # Example: Execute a query
    records = hook.get_records("SELECT * FROM transactions LIMIT 10;")
    print(records)
    # Example: Execute a DML statement
    # hook.run("INSERT INTO another_table (col1) VALUES ('test');")

@dag(
    dag_id='test_mysql_connection',
    start_date=datetime(2023, 1, 1),
    schedule="@once",
    catchup=False,
    tags=['mysql'],
)
def mysql_connection_dag():
    query_task = PythonOperator(
        task_id='fetch_data_from_mysql',
        python_callable=_query_data,
        op_kwargs={'conn_id': 'mysql'}, # Use your defined connection ID here
    )

mysql_connection_dag()
