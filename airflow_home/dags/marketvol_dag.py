from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta, date
import yfinance as yf
import os

def download_data(symbol, **kwargs):
    exec_date = kwargs['ds']
    dir_path = f"/tmp/data/{exec_date}"
    os.makedirs(dir_path, exist_ok=True)
    start_date = date.today()
    end_date = start_date + timedelta(days=1)
    df = yf.download(symbol, start=start_date, end=end_date, interval='1m')
    df.to_csv(f"{dir_path}/{symbol}.csv", header=False)

def run_query(**kwargs):
    exec_date = kwargs['ds']
    dir_path = f"/tmp/data/{exec_date}"
    with open(f"{dir_path}/AAPL.csv", 'r') as f1, open(f"{dir_path}/TSLA.csv", 'r') as f2:
        aapl_lines = sum(1 for _ in f1)
        tsla_lines = sum(1 for _ in f2)
    print(f"AAPL rows: {aapl_lines}, TSLA rows: {tsla_lines}")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.combine(datetime.today(), datetime.min.time()).replace(hour=18),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'marketvol',
    default_args=default_args,
    description='Download and analyze AAPL and TSLA stock data',
    schedule='0 18 * * 1-5',
    catchup=True,
)

create_dir = BashOperator(
    task_id='t0',
    bash_command='mkdir -p /tmp/data/{{ ds }}',
    dag=dag
)

download_aapl = PythonOperator(
    task_id='t1',
    python_callable=download_data,
    op_kwargs={'symbol': 'AAPL'},
    dag=dag
)

download_tsla = PythonOperator(
    task_id='t2',
    python_callable=download_data,
    op_kwargs={'symbol': 'TSLA'},
    dag=dag
)

analyze_data = PythonOperator(
    task_id='t5',
    python_callable=run_query,
    dag=dag
)

create_dir >> [download_aapl, download_tsla] >> analyze_data
