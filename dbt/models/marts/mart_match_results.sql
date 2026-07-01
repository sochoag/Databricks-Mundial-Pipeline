with matches as (
    select * from {{ ref('stg_matches') }}
),

teams as (
    select team_id, team_name, team_tla, crest_url, country_code
    from {{ ref('stg_teams') }}
)

select
    m.match_id,
    m.match_date,
    m.matchday,
    m.stage,
    m.status,
    m.home_team_id,
    ht.team_name                    as home_team_name,
    ht.team_tla                     as home_team_tla,
    ht.crest_url                    as home_team_crest,
    ht.country_code                 as home_country_code,
    m.away_team_id,
    at_.team_name                   as away_team_name,
    at_.team_tla                    as away_team_tla,
    at_.crest_url                   as away_team_crest,
    at_.country_code                as away_country_code,
    m.home_goals,
    m.away_goals,
    m.home_goals + m.away_goals     as total_goals,
    m.winner,
    m.duration
from matches m
left join teams ht  on m.home_team_id = ht.team_id
left join teams at_ on m.away_team_id = at_.team_id
order by m.match_date
