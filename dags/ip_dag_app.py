import time
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Add the src directory to the path
sys.path.append("/opt/airflow/src")

from ingestion_app import fetch_ips_from_queue
from enrichment_app import enrich_ip
from storage import connect_db, create_table, insert_data

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="ip_queue_pipeline",
    default_args=default_args,
    schedule_interval="*/10 * * * *",  # Every 10 minutes
    start_date=datetime(2025, 8, 5),
    catchup=False,
    tags=["geolocation", "ipstack", "queue"]
) as dag:

    def ingest_task():
        return fetch_ips_from_queue(count=10)

    def enrich_task(ti):
        ip_list = ti.xcom_pull(task_ids="ingest")
        enriched = []
        for ip in ip_list:
            result = enrich_ip(ip)
            if result:
                enriched.append(result)
            time.sleep(1)  # To manage IPStack API rate limits
        return enriched

    def store_task(ti):
        enriched_data = ti.xcom_pull(task_ids="enrich")

        if not enriched_data or len(enriched_data) == 0:
            print("No enriched data to store.")
            return

        conn = connect_db()
        if conn:
            create_table(conn)
            insert_data(conn, enriched_data)
            conn.close()
            print(f"Stored {len(enriched_data)} records in PostgreSQL.")
        else:
            raise ValueError("Database connection failed")

    ingest = PythonOperator(
        task_id="ingest",
        python_callable=ingest_task
    )

    enrich = PythonOperator(
        task_id="enrich",
        python_callable=enrich_task
    )

    store = PythonOperator(
        task_id="store",
        python_callable=store_task
    )

    ingest >> enrich >> store
