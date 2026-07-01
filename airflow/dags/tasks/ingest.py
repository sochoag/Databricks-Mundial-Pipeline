import json
import os
import logging
from datetime import datetime
from pathlib import Path

import requests

logger = logging.getLogger(__name__)

API_KEY = os.environ["FOOTBALL_API_KEY"]
BASE_URL = os.environ.get("FOOTBALL_API_BASE_URL", "https://api.football-data.org/v4")
HEADERS = {"X-Auth-Token": API_KEY}

# Copa del Mundo 2022 = competition code WC, season 2022
WORLD_CUP_ID = 2000
OUTPUT_DIR = Path("/tmp/mundial")


def _fetch(endpoint: str) -> dict:
    url = f"{BASE_URL}{endpoint}"
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return resp.json()


def _save(data: dict, filename: str) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / filename
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    logger.info("Saved %s (%d bytes)", path, path.stat().st_size)
    return path


def ingest_competitions(**kwargs) -> str:
    data = _fetch("/competitions/WC")
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    path = _save(data, f"competition_{ts}.json")
    return str(path)


def ingest_teams(**kwargs) -> str:
    data = _fetch(f"/competitions/WC/teams?season=2022")
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    path = _save(data, f"teams_{ts}.json")
    return str(path)


def ingest_matches(**kwargs) -> str:
    data = _fetch(f"/competitions/WC/matches?season=2022")
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    path = _save(data, f"matches_{ts}.json")
    return str(path)


def ingest_standings(**kwargs) -> str:
    data = _fetch(f"/competitions/WC/standings?season=2022")
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    path = _save(data, f"standings_{ts}.json")
    return str(path)
