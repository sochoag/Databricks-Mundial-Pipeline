# Databricks notebook: Mundial - Raw → Curated Transform
# Reads JSON from S3 raw layer, cleans, writes Delta to curated layer

# COMMAND ----------
import json
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import *
from delta.tables import DeltaTable

spark = SparkSession.builder.getOrCreate()

# COMMAND ----------
# Config — override via Databricks job parameters if needed
S3_ENDPOINT   = dbutils.widgets.get("s3_endpoint") if "s3_endpoint" in [w.name for w in dbutils.widgets.getAll()] else "http://localstack:4566"
RAW_BUCKET    = "s3a://mundial-raw"
CURATED_PATH  = "s3a://mundial-curated"

spark.conf.set("fs.s3a.endpoint", S3_ENDPOINT)
spark.conf.set("fs.s3a.access.key", "test")
spark.conf.set("fs.s3a.secret.key", "test")
spark.conf.set("fs.s3a.path.style.access", "true")

# COMMAND ----------
# ── Matches ──────────────────────────────────────────────────────────────────
raw_matches = (
    spark.read
    .option("multiline", "true")
    .json(f"{RAW_BUCKET}/matches/")
)

matches_exploded = raw_matches.select(
    F.explode("matches").alias("m")
).select(
    F.col("m.id").alias("match_id"),
    F.col("m.utcDate").alias("match_date"),
    F.col("m.status"),
    F.col("m.matchday"),
    F.col("m.stage"),
    F.col("m.homeTeam.id").alias("home_team_id"),
    F.col("m.homeTeam.name").alias("home_team_name"),
    F.col("m.awayTeam.id").alias("away_team_id"),
    F.col("m.awayTeam.name").alias("away_team_name"),
    F.col("m.score.fullTime.home").alias("home_goals"),
    F.col("m.score.fullTime.away").alias("away_goals"),
    F.col("m.score.winner").alias("winner"),
    F.col("m.score.duration").alias("duration"),
).filter(F.col("status") == "FINISHED")

matches_exploded.write.format("delta").mode("overwrite").save(f"{CURATED_PATH}/matches/")
print(f"Matches written: {matches_exploded.count()} rows")

# COMMAND ----------
# ── Teams ─────────────────────────────────────────────────────────────────────
raw_teams = (
    spark.read
    .option("multiline", "true")
    .json(f"{RAW_BUCKET}/teams/")
)

teams_clean = raw_teams.select(
    F.explode("teams").alias("t")
).select(
    F.col("t.id").alias("team_id"),
    F.col("t.name").alias("team_name"),
    F.col("t.shortName").alias("team_short_name"),
    F.col("t.tla").alias("team_tla"),
    F.col("t.crestUrl").alias("crest_url"),
    F.col("t.area.name").alias("country"),
    F.col("t.area.code").alias("country_code"),
    F.col("t.founded"),
    F.col("t.venue"),
)

teams_clean.write.format("delta").mode("overwrite").save(f"{CURATED_PATH}/teams/")
print(f"Teams written: {teams_clean.count()} rows")

# COMMAND ----------
# ── Standings ─────────────────────────────────────────────────────────────────
raw_standings = (
    spark.read
    .option("multiline", "true")
    .json(f"{RAW_BUCKET}/standings/")
)

standings_clean = raw_standings.select(
    F.explode("standings").alias("s")
).select(
    F.col("s.stage"),
    F.col("s.type"),
    F.col("s.group").alias("group_name"),
    F.explode("s.table").alias("entry"),
).select(
    "stage", "type", "group_name",
    F.col("entry.position"),
    F.col("entry.team.id").alias("team_id"),
    F.col("entry.team.name").alias("team_name"),
    F.col("entry.playedGames").alias("played_games"),
    F.col("entry.won"),
    F.col("entry.draw"),
    F.col("entry.lost"),
    F.col("entry.points"),
    F.col("entry.goalsFor").alias("goals_for"),
    F.col("entry.goalsAgainst").alias("goals_against"),
    F.col("entry.goalDifference").alias("goal_difference"),
)

standings_clean.write.format("delta").mode("overwrite").save(f"{CURATED_PATH}/standings/")
print(f"Standings written: {standings_clean.count()} rows")

# COMMAND ----------
display(matches_exploded.limit(5))
display(teams_clean.limit(5))
display(standings_clean.limit(5))
