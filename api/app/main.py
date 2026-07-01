from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import teams, matches, standings, pipeline

app = FastAPI(
    title="Mundial de Datos API",
    description="API que sirve estadisticas del Mundial 2022 procesadas via Airflow + Databricks + dbt",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(teams.router, prefix="/teams", tags=["teams"])
app.include_router(matches.router, prefix="/matches", tags=["matches"])
app.include_router(standings.router, prefix="/standings", tags=["standings"])
app.include_router(pipeline.router, prefix="/pipeline", tags=["pipeline"])


@app.get("/health")
def health():
    return {"status": "ok"}
