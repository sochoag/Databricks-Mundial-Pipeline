with standings as (
    select * from {{ ref('stg_standings') }}
    where type = 'TOTAL' and stage = 'GROUP_STAGE'
),

teams as (
    select team_id, crest_url, country_code
    from {{ ref('stg_teams') }}
)

select
    s.group_name,
    s.position,
    s.team_id,
    s.team_name,
    t.crest_url,
    t.country_code,
    s.played_games,
    s.won,
    s.draw,
    s.lost,
    s.points,
    s.goals_for,
    s.goals_against,
    s.goal_difference
from standings s
left join teams t on s.team_id = t.team_id
order by s.group_name, s.position
