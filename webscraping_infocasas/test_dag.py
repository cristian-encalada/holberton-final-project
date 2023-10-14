# Airflow script

import subprocess
from datetime import datetime
from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import logging

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['martinleiro9@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'catchup': False
}

def scraping_infocasas():
    logging.info('performing infocasas')
    subprocess.run(['python3', 'root/Alquivago/webscraping/webscraping_infocasas/S_infocasas_d04.py'])

def scraping_gallito():
    logging.info('performing gallito')
    subprocess.run(['python3', 'root/Alquivago/webscraping/webscraping_gallito/S_gallito_d03.py'])


# cada scraping debe ejecutarse como tarea independiente
# debe respetarse el turno de ejecucion en el navegador de chrome 

with DAG(
    'dag_infocasas',
    default_args=default_args,
    description='Scraping infocasas',
    schedule_interval = '0 */8 * * *',
    start_date=datetime(2023, 10, 1),
    catchup=False,
    tags=['infocasas']
) as dag:
    scraping_infocasas_task = PythonOperator(task_id="S_infocasas", python_callable=scraping_infocasas)

with DAG(
    'dag_gallito',
    default_args=default_args,
    description='Scraping gallito',
    schedule_interval = '0 */6 * * *',
    start_date=datetime(2023, 10, 1),
    catchup=False,
    tags=['gallito']
) as dag:
    scraping_gallito_task = PythonOperator(task_id="S_gallito", python_callable=scraping_gallito)