# Airflow script

import logging
import subprocess

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago


default_args = {
    'owner': 'alquivago',
    'start_date': datetime(2023, 11, 2),
    'email': ['..@mail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'catchup': False
}


def scraping_infocasas():
    subprocess.run(['python3', '/root/Alquivago/webscraping/webscraping_infocasas/S_infocasas_v00.py'])

def scraping_gallito():
    subprocess.run(['python3', '/root/Alquivago/webscraping/webscraping_gallito/S_gallito_v00.py'])

def api_mercadolibre():
    subprocess.run(['python3', '/root/Alquivago/api_mercadolibre/extract_properties.py'])

def subida_a_github():
    subprocess.run(['python3', '/root/Alquivago/webscraping/upload.py'])


with DAG(
    'dag_upload',
    default_args=default_args,
    description='data update',
    schedule_interval=None, # manual
    tags=['upload']
) as dag:
    PythonOperator(task_id="update_data", python_callable=subida_a_github)


with DAG(
    'dag_mercadolibre',
    default_args=default_args,
    description='Extract mercadolibre',
    schedule_interval=timedelta(hours=1),
    # schedule_interval=None,
    tags=['mercadolibre']
) as dag:
    api_mercadolibre_task = PythonOperator(task_id="api_mercadolibre", python_callable=api_mercadolibre)
    upload_data_task = PythonOperator(task_id="upload", python_callable=subida_a_github)
    api_mercadolibre_task >> upload_data_task


with DAG(
    'dag_infocasas',
    default_args=default_args,
    description='Scraping infocasas',
    schedule_interval=timedelta(hours=4),
    # schedule_interval=None,
    tags=['infocasas']
) as dag:
    scraping_infocasas_task = PythonOperator(task_id="S_infocasas", python_callable=scraping_infocasas)
    upload_data_task = PythonOperator(task_id="upload", python_callable=subida_a_github)
    scraping_infocasas_task >> upload_data_task


with DAG(
    'dag_gallito',
    default_args=default_args,
    description='Scraping gallito',
    schedule_interval=timedelta(hours=2),
    # schedule_interval=None,
    tags=['gallito']
) as dag:
    scraping_gallito_task = PythonOperator(task_id="S_gallito", python_callable=scraping_gallito)
    upload_data_task = PythonOperator(task_id="upload", python_callable=subida_a_github)
    scraping_gallito_task >> upload_data_task
