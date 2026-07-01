# Mundial de Datos — Data Engineering Portfolio

A full-stack data engineering portfolio built around the **FIFA World Cup Qatar 2022**, featuring an interactive 3D globe and a production-grade data pipeline. The goal is to demonstrate end-to-end data engineering skills — from ingestion to serving — not just frontend aesthetics.

---

## Architecture

```
football-data.org API
        │
        ▼
   Apache Airflow       ← orchestration
        │
        ▼
   LocalStack S3        ← raw JSON (mundial-raw bucket)
        │
        ▼
   Databricks + PySpark ← transformation → Delta Lake (mundial-curated)
        │
        ▼
      dbt models        ← staging views + analytics marts (mundial-analytics)
        │
        ▼
      FastAPI           ← serves Parquet files via REST
        │
        ▼
   Next.js + Three.js   ← interactive 3D globe frontend
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Orchestration | Apache Airflow 2.9 (Docker) |
| Data Source | football-data.org API v4 |
| Storage | AWS S3 via LocalStack 3.5 |
| IaC | Terraform (runs via Docker, no local install needed) |
| Compute / Transform | Databricks Community Edition + PySpark + Delta Lake |
| Data Modeling | dbt-databricks 1.8 |
| API Serving | FastAPI |
| Frontend | Next.js + Three.js + Tailwind CSS |
| Local Environment | Docker Compose |

---

## Data Layers

| Bucket | Content |
|---|---|
| `mundial-raw` | Raw JSON from the API, partitioned by entity and date |
| `mundial-curated` | Delta Tables processed by PySpark on Databricks |
| `mundial-analytics` | Final Parquet files served by FastAPI |

### dbt Models

**Staging**
- `stg_matches` — raw match results
- `stg_teams` — team metadata
- `stg_standings` — group standings

**Marts**
- `mart_team_stats` — aggregated team performance
- `mart_match_results` — cleaned match data
- `mart_group_standings` — final group tables

---

## Project Structure

```
.
├── airflow/
│   ├── dags/
│   │   ├── mundial_pipeline.py   # main DAG
│   │   └── tasks/
│   └── Dockerfile
├── api/                          # FastAPI app
├── databricks/
│   └── notebooks/                # PySpark transformation notebooks
├── dbt/
│   ├── models/
│   │   ├── staging/
│   │   └── marts/
│   └── dbt_project.yml
├── frontend/                     # Next.js + Three.js app
├── infra/                        # Terraform (S3 buckets + IAM via LocalStack)
├── docker-compose.yml
└── Makefile
```

---

## Getting Started

### Prerequisites

- Docker & Docker Compose
- A free API key from [football-data.org](https://www.football-data.org/)
- A [Databricks Community Edition](https://community.cloud.databricks.com/) account

### 1. Environment setup

```bash
cp .env.example .env
# Fill in FOOTBALL_DATA_API_KEY and Databricks credentials
```

### 2. Start the full stack

```bash
make up
```

| Service | URL |
|---|---|
| Airflow UI | http://localhost:8080 (admin / admin) |
| FastAPI docs | http://localhost:8000/docs |
| Frontend | http://localhost:3000 |

### 3. Provision infrastructure (LocalStack S3 buckets)

```bash
make infra-init
make infra-apply
```

### 4. Run the Airflow pipeline

Trigger the `mundial_pipeline` DAG from the Airflow UI at http://localhost:8080. It will fetch data from the API and land it in the `mundial-raw` S3 bucket.

### 5. Run Databricks transformations

Upload `databricks/notebooks/01_curated_transform.py` to your Databricks Community Edition workspace and run it. It reads from `mundial-raw`, applies PySpark transformations, and writes Delta Tables to `mundial-curated`.

### 6. Run dbt models

```bash
make dbt-run
make dbt-test
```

### All Make commands

```bash
make help
```

---

## Screenshots

> Coming soon — 3D globe with team stats overlay.

---

## License

MIT
