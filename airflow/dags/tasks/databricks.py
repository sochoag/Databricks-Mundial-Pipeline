import os
import time
import logging

import requests

logger = logging.getLogger(__name__)

DATABRICKS_HOST = os.environ.get("DATABRICKS_HOST", "")
DATABRICKS_TOKEN = os.environ.get("DATABRICKS_TOKEN", "")
JOB_NAME = "mundial-curated-transform"


def _headers() -> dict:
    return {"Authorization": f"Bearer {DATABRICKS_TOKEN}"}


def _get_job_id() -> int | None:
    resp = requests.get(
        f"{DATABRICKS_HOST}/api/2.1/jobs/list",
        headers=_headers(),
        params={"name": JOB_NAME},
        timeout=30,
    )
    resp.raise_for_status()
    jobs = resp.json().get("jobs", [])
    return jobs[0]["job_id"] if jobs else None


def trigger_databricks_job(**kwargs) -> None:
    if not DATABRICKS_HOST or not DATABRICKS_TOKEN:
        logger.warning("Databricks credentials not set — skipping transformation step")
        return

    job_id = _get_job_id()
    if job_id is None:
        logger.warning("Databricks job '%s' not found — skipping", JOB_NAME)
        return

    run_resp = requests.post(
        f"{DATABRICKS_HOST}/api/2.1/jobs/run-now",
        headers=_headers(),
        json={"job_id": job_id},
        timeout=30,
    )
    run_resp.raise_for_status()
    run_id = run_resp.json()["run_id"]
    logger.info("Triggered Databricks run %s", run_id)

    # Poll until complete (max 20 min)
    for _ in range(120):
        time.sleep(10)
        state_resp = requests.get(
            f"{DATABRICKS_HOST}/api/2.1/jobs/runs/get",
            headers=_headers(),
            params={"run_id": run_id},
            timeout=30,
        )
        state_resp.raise_for_status()
        life_cycle = state_resp.json()["state"]["life_cycle_state"]
        logger.info("Databricks run %s state: %s", run_id, life_cycle)

        if life_cycle == "TERMINATED":
            result = state_resp.json()["state"]["result_state"]
            if result != "SUCCESS":
                raise RuntimeError(f"Databricks run {run_id} ended with: {result}")
            return

    raise TimeoutError(f"Databricks run {run_id} did not finish in 20 minutes")
