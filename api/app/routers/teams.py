from fastapi import APIRouter, HTTPException
from app.s3 import read_parquet

router = APIRouter()


@router.get("/")
def get_teams():
    try:
        df = read_parquet("marts/mart_team_stats/data.parquet")
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Data not available: {e}")


@router.get("/{team_id}")
def get_team(team_id: int):
    try:
        df = read_parquet("marts/mart_team_stats/data.parquet")
        row = df[df["team_id"] == team_id]
        if row.empty:
            raise HTTPException(status_code=404, detail="Team not found")
        return row.iloc[0].to_dict()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Data not available: {e}")
