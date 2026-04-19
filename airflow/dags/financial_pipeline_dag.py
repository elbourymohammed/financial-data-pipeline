from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime, timedelta
import sys
import os

sys.path.append('/Users/elbourymohammed/Desktop/Data_Project/src')

base_path: str = '/Users/elbourymohammed/Desktop/Data_Project/src/scripts/'

default_args = {
    'owner' : 'admin',
    'retries' : 1,
    'retry_delay' : timedelta(minutes=5)
}

with DAG (
    dag_id = "financial_mart",
    default_args=default_args,
    description="Ingestion, transformation and test data",
    schedule="0 0 * * FRI",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['finance', 'metals', 'crypto'],
) as dag:

    init_db = BashOperator(
        bash_command=f'python3 {base_path}/init_db.py',
        task_id="initialisation_de_bdd"
    )
    
    ingest_crypto = BashOperator(
        bash_command=f'python3 {base_path}/ingest_crypto.py',
        task_id="ingest_crypto_data"
    )

    ingest_fx_rates = BashOperator(
        bash_command=f'python3 {base_path}/ingest_fx_rates.py',
        task_id="ingest_fx_rates_data"
    )

    ingest_macro_indicators = BashOperator(
        bash_command=f'python3 {base_path}/ingest_macro_indicators.py',
        task_id="ingest_macro_indicators_data"
    )

    ingest_metal = BashOperator(
        bash_command=f'python3 {base_path}/ingest_metal.py',
        task_id="ingest_metal_data"
    )

    dbt_transformation = BashOperator(
        bash_command=f'cd /Users/elbourymohammed/Desktop/Data_Project/metal_project && dbt run',
        task_id="dbt_transformation"
    )

    dbt_test = BashOperator(
        bash_command=f'cd /Users/elbourymohammed/Desktop/Data_Project/metal_project && dbt test',
        task_id="dbt_tests"
    )

    pipeline = init_db >> [ingest_macro_indicators, ingest_crypto, ingest_fx_rates, ingest_metal] >> dbt_transformation >> dbt_test