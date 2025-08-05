# from airflow import DAG
# from airflow.operators.python import PythonOperator
# from datetime import datetime
# import sys
# import os

# # Add the src directory to the path
# sys.path.append("/opt/airflow/src")

# from ingestion import load_ip_addresses
# from enrichment import enrich_ip
# from storage import connect_db, create_table, insert_data

# default_args = {
#     "owner": "airflow",
#     "start_date": datetime(2024, 1, 1),
#     "retries": 1
# }

# with DAG(
#     dag_id="geolocation_pipeline",
#     default_args=default_args,
#     schedule_interval="@daily",
#     catchup=False,
#     tags=["geolocation", "ipstack"]
# ) as dag:

#     def ingest_task():
#         return load_ip_addresses("/opt/airflow/data/sample_of_logs.txt")

#     def enrich_task(ti):
#         ip_list = ti.xcom_pull(task_ids="ingest")
#         enriched = [enrich_ip(ip) for ip in ip_list]
#         return enriched
    
#     def store_task(ti):
#         enriched_data = ti.xcom_pull(task_ids="enrich")

#         print("DB_HOST seen by DAG:", os.getenv("DB_HOST"))

#         conn = connect_db()
#         if conn:
#             create_table(conn)
#             insert_data(conn, enriched_data)
#             conn.close()
#         else:
#             raise ValueError("Database connection failed")

#     ingest = PythonOperator(
#         task_id="ingest",
#         python_callable=ingest_task
#     )

#     enrich = PythonOperator(
#         task_id="enrich",
#         python_callable=enrich_task
#     )

#     store = PythonOperator(
#         task_id="store",
#         python_callable=store_task
#     )

#     ingest >> enrich >> store


# from airflow import DAG
# from airflow.operators.python import PythonOperator
# from datetime import datetime, timedelta
# import sys
# import os

# # Add the src directory to the path
# sys.path.append("/opt/airflow/src")

# from ingestion import load_ip_addresses
# from enrichment import enrich_ip
# from storage import connect_db, create_table, insert_data

# default_args = {
#     "owner": "airflow",
#     "depends_on_past": False,
#     "retries": 1,
#     "retry_delay": timedelta(minutes=2),
# }

# with DAG(
#     dag_id="geolocation_pipeline",
#     default_args=default_args,
#     schedule_interval="*/10 * * * *",
#     start_date=datetime(2025, 7, 1),
#     catchup=False,
#     tags=["geolocation", "ipstack"]
# ) as dag:

#     # def ingest_task():
#     #     return load_ip_addresses("/opt/airflow/data/sample_of_logs.txt")
#     def ingest_task():
#         return load_ip_addresses()


#     def enrich_task(ti):
#         ip_list = ti.xcom_pull(task_ids="ingest")
#         enriched = [enrich_ip(ip) for ip in ip_list]
#         return enriched
    
#     def store_task(ti):
#         enriched_data = ti.xcom_pull(task_ids="enrich")
#         print("DB_HOST seen by DAG:", os.getenv("DB_HOST"))
#         conn = connect_db()
#         if conn:
#             create_table(conn)
#             insert_data(conn, enriched_data)
#             conn.close()
#         else:
#             raise ValueError("Database connection failed")

#     ingest = PythonOperator(
#         task_id="ingest",
#         python_callable=ingest_task
#     )

#     enrich = PythonOperator(
#         task_id="enrich",
#         python_callable=enrich_task
#     )

#     store = PythonOperator(
#         task_id="store",
#         python_callable=store_task
#     )

#     ingest >> enrich >> store

import time 

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Add the src directory to the path
sys.path.append("/opt/airflow/src")

from ingestion import load_ip_addresses
from enrichment import enrich_ip
from storage import connect_db, create_table, insert_data

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="geolocation_pipeline",
    default_args=default_args,
    schedule_interval="*/10 * * * *",  # Every 10 minutes
    start_date=datetime(2025, 7, 1),
    catchup=False,
    tags=["geolocation", "ipstack"]
) as dag:

    def ingest_task():
        return load_ip_addresses()  # Generate random IPs

    # def enrich_task(ti):
    #     ip_list = ti.xcom_pull(task_ids="ingest")
    #     enriched = [enrich_ip(ip) for ip in ip_list]
    #     # Filter out None values to avoid errors in store step
    #     valid_enriched = [e for e in enriched if e is not None]
    #     return valid_enriched

    def enrich_task(ti):
        ip_list = ti.xcom_pull(task_ids="ingest")
        enriched = []
        for ip in ip_list:
            result = enrich_ip(ip)
            if result:
                enriched.append(result)
            time.sleep(1)  # Limit IPStack rate 
        return enriched

    def store_task(ti):
        enriched_data = ti.xcom_pull(task_ids="enrich")

        if not enriched_data or len(enriched_data) == 0:
            print("⚠️ No enriched data to store.")
            return

        print("DB_HOST seen by DAG:", os.getenv("DB_HOST"))
        conn = connect_db()
        if conn:
            create_table(conn)
            insert_data(conn, enriched_data)
            conn.close()
            print(f"✅ Stored {len(enriched_data)} records in PostgreSQL.")
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
