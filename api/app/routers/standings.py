from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from app.s3 import read_parquet

router = APIRouter()


@router.get("/")
def get_standings(group: Optional[str] = Query(None)):
    try:
        df = read_parquet("marts/mart_group_standings/data.parquet")
        if group:
            df = df[df["group_name"] == group.upper()]
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Data not available: {e}")


@router.get("/groups")
def get_groups():
    try:
        df = read_parquet("marts/mart_group_standings/data.parquet")
        return sorted(df["group_name"].unique().tolist())
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Data not available: {e}")
