from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

PROJECT_HOME = "...../BCRA" #Ruta absoluta
PYTHON_ENV = "source /RUTA/A/CONDA/bin/activate TU_ENTORNO" #para activar el entorno

default_args = {
    "owner": "data_engineer",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": False,
}

with DAG(
    dag_id="dollar_pipeline",
    default_args=default_args,
    start_date=datetime(2026, 3, 25),
    schedule_interval="@daily",
    catchup=False
) as dag:

    ingesta_task = BashOperator(
        task_id='ingesta_bronze',
        bash_command=f'{PYTHON_ENV} && python -m jobs.ingesta',
        cwd=PROJECT_HOME 
    )

    clean_task = BashOperator(
        task_id='clean_silver',
        bash_command=f'{PYTHON_ENV} && python -m jobs.clean',
        cwd=PROJECT_HOME
    )

    agg_task = BashOperator(
        task_id='agg_gold',
        bash_command=f'{PYTHON_ENV} && python -m jobs.agg',
        cwd=PROJECT_HOME
    )

    ingesta_task >> clean_task >> agg_task