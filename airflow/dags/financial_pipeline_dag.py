from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

DBT_PATH: str = str(os.getenv('DBT_PATH'))
sys.path.insert(0, DBT_PATH)

# Import des runners pour l'ingestion
from runners.crypto_runner import run as run_crypto
from runners.fx_rates_runner import run as run_fx
from runners.macro_indicators_runner import run as run_macro
from runners.metal_runner import run as run_metal


default_args = {
    'owner': 'admin',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='financial_pipeline',
    default_args=default_args,
    description='Financial data ingestion and transformation pipeline',
    schedule='0 0 * * *',
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['finance', 'metals', 'crypto'],
) as dag:

    # Ingestion des données pour la veille
    # Chaque runner récupère automatiquement la date d'hier
    ingest_crypto = PythonOperator(
        task_id='ingest_crypto',
        python_callable=run_crypto,
    )

    ingest_fx = PythonOperator(
        task_id='ingest_fx_rates',
        python_callable=run_fx,
    )

    ingest_macro = PythonOperator(
        task_id='ingest_macro_indicators',
        python_callable=run_macro,
    )

    ingest_metal = PythonOperator(
        task_id='ingest_metal',
        python_callable=run_metal,
    )

    # DBT transformation
    dbt_transformation = BashOperator(
        task_id='dbt_transformation',
        bash_command=f'cd {DBT_PATH} && dbt run --full-refresh',
    )

    dbt_test = BashOperator(
        task_id='dbt_tests',
        bash_command=f'cd {DBT_PATH} && dbt test',
    )

    # Pipeline: ingestion en parallèle -> DBT
    [ingest_crypto, ingest_fx, ingest_macro, ingest_metal] >> dbt_transformation >> dbt_test