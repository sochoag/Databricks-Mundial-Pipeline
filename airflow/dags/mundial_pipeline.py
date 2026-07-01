from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

from tasks.ingest import ingest_competitions, ingest_teams, ingest_matches, ingest_standings
from tasks.upload import upload_to_s3
from tasks.databricks import trigger_databricks_job

default_args = {
    "owner": "mundial",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": False,
}

with DAG(
    dag_id="mundial_pipeline",
    description="Ingesta, transformacion y carga de datos del Mundial",
    default_args=default_args,
    start_date=days_ago(1),
    schedule_interval="0 6 * * *",  # diario a las 6am
    catchup=False,
    tags=["mundial", "ingestion", "dbt", "databricks"],
) as dag:

    # ── Extraccion desde API ───────────────────────────────────
    t_competitions = PythonOperator(
        task_id="ingest_competitions",
        python_callable=ingest_competitions,
    )

    t_teams = PythonOperator(
        task_id="ingest_teams",
        python_callable=ingest_teams,
    )

    t_matches = PythonOperator(
        task_id="ingest_matches",
        python_callable=ingest_matches,
    )

    t_standings = PythonOperator(
        task_id="ingest_standings",
        python_callable=ingest_standings,
    )

    # ── Upload a S3 raw layer ──────────────────────────────────
    t_upload = PythonOperator(
        task_id="upload_raw_to_s3",
        python_callable=upload_to_s3,
    )

    # ── Databricks: limpieza y curated layer ──────────────────
    t_databricks = PythonOperator(
        task_id="trigger_databricks_transformation",
        python_callable=trigger_databricks_job,
    )

    # ── dbt: modelos analytics ─────────────────────────────────
    t_dbt = BashOperator(
        task_id="dbt_run",
        bash_command=(
            "cd /opt/airflow/dags/../.. && "
            "dbt run --profiles-dir /opt/airflow/dbt --project-dir /opt/airflow/dbt"
        ),
    )

    t_dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=(
            "cd /opt/airflow/dags/../.. && "
            "dbt test --profiles-dir /opt/airflow/dbt --project-dir /opt/airflow/dbt"
        ),
    )

    # ── Dependencias ──────────────────────────────────────────
    [t_competitions, t_teams, t_matches, t_standings] >> t_upload
    t_upload >> t_databricks >> t_dbt >> t_dbt_test
