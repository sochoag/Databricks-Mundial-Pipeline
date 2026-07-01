from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from app.s3 import read_parquet

router = APIRouter()


@router.get("/")
def get_matches(stage: Optional[str] = Query(None)):
    try:
        df = read_parquet("marts/mart_match_results/data.parquet")
        if stage:
            df = df[df["stage"] == stage.upper()]
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Data not available: {e}")


@router.get("/stages")
def get_stages():
    try:
        df = read_parquet("marts/mart_match_results/data.parquet")
        return sorted(df["stage"].unique().tolist())
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Data not available: {e}")
