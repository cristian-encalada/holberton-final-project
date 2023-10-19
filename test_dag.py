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
    subprocess.run(['python3', 'root/Alquivago/webscraping/webscraping_infocasas/S_infocasas_v00.py'])

def scraping_gallito():
    logging.info('performing gallito')
    subprocess.run(['python3', 'root/Alquivago/webscraping/webscraping_gallito/S_gallito_v00.py'])

def subida_a_github():
    logging.info('performing update data')
    subprocess.run(['python3', 'root/Alquivago/webscraping/upload.py'])

# cada scraping debe ejecutarse como tarea independiente
# debe respetarse el turno de ejecucion en el navegador

with DAG(
    'dag_infocasas',
    default_args=default_args,
    description='Scraping infocasas',
    schedule_interval = '0 */3 * * *',
    start_date=datetime(2023, 10, 1),
    catchup=False,
    tags=['infocasas']
) as dag:
    scraping_infocasas_task = PythonOperator(task_id="S_infocasas", python_callable=scraping_infocasas)

with DAG(
    'dag_gallito',
    default_args=default_args,
    description='Scraping gallito',
    schedule_interval = '0 */2 * * *',
    start_date=datetime(2023, 10, 1),
    catchup=False,
    tags=['gallito']
) as dag:
    scraping_gallito_task = PythonOperator(task_id="S_gallito", python_callable=scraping_gallito)

with DAG(
    'dag_upload_data',
    default_args=default_args,
    description='upload data',
    schedule_interval = '0 */4 * * *',
    start_date=datetime(2023, 10, 1),
    catchup=False,
    tags=['upload']
) as dag:
    upload_data_task = PythonOperator(task_id="upload", python_callable=subida_a_github)
