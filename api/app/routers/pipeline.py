from fastapi import APIRouter

router = APIRouter()

STACK = {
    "ingestion": {
        "tool": "Apache Airflow 2.9",
        "description": "DAG diario que consume football-data.org y sube JSON a S3 raw layer",
        "dag": "mundial_pipeline",
        "schedule": "0 6 * * *",
    },
    "storage": {
        "tool": "AWS S3 (LocalStack)",
        "description": "Data lake con 3 capas: raw (JSON), curated (Delta), analytics (Parquet)",
        "buckets": ["mundial-raw", "mundial-curated", "mundial-analytics"],
        "iac": "Terraform",
    },
    "transformation": {
        "tool": "Databricks + Apache Spark",
        "description": "Notebook PySpark que limpia y escribe Delta Tables desde raw hacia curated",
        "format": "Delta Lake",
    },
    "modeling": {
        "tool": "dbt-databricks",
        "description": "Modelos SQL: staging (views) + marts (tables). Tests de calidad incluidos.",
        "models": ["stg_matches", "stg_teams", "stg_standings",
                   "mart_team_stats", "mart_match_results", "mart_group_standings"],
    },
    "serving": {
        "tool": "FastAPI",
        "description": "API REST que lee Parquet desde S3 analytics y sirve al frontend",
        "endpoints": ["/teams", "/matches", "/standings"],
    },
    "frontend": {
        "tool": "Next.js + Three.js",
        "description": "Globo 3D interactivo con estadisticas del Mundial por pais",
    },
}


@router.get("/")
def get_stack():
    return STACK
