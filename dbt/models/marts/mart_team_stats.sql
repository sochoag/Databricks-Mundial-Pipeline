with matches as (
    select * from {{ ref('stg_matches') }}
),

teams as (
    select * from {{ ref('stg_teams') }}
),

home_stats as (
    select
        home_team_id        as team_id,
        count(*)            as home_games,
        sum(home_goals)     as home_goals_scored,
        sum(away_goals)     as home_goals_conceded,
        sum(case when winner = 'HOME_TEAM' then 1 else 0 end) as home_wins,
        sum(case when winner = 'DRAW' then 1 else 0 end)      as home_draws,
        sum(case when winner = 'AWAY_TEAM' then 1 else 0 end) as home_losses
    from matches
    group by home_team_id
),

away_stats as (
    select
        away_team_id        as team_id,
        count(*)            as away_games,
        sum(away_goals)     as away_goals_scored,
        sum(home_goals)     as away_goals_conceded,
        sum(case when winner = 'AWAY_TEAM' then 1 else 0 end) as away_wins,
        sum(case when winner = 'DRAW' then 1 else 0 end)      as away_draws,
        sum(case when winner = 'HOME_TEAM' then 1 else 0 end) as away_losses
    from matches
    group by away_team_id
),

combined as (
    select
        coalesce(h.team_id, a.team_id)                               as team_id,
        coalesce(h.home_games, 0) + coalesce(a.away_games, 0)       as total_games,
        coalesce(h.home_wins, 0) + coalesce(a.away_wins, 0)         as total_wins,
        coalesce(h.home_draws, 0) + coalesce(a.away_draws, 0)       as total_draws,
        coalesce(h.home_losses, 0) + coalesce(a.away_losses, 0)     as total_losses,
        coalesce(h.home_goals_scored, 0) + coalesce(a.away_goals_scored, 0)     as goals_scored,
        coalesce(h.home_goals_conceded, 0) + coalesce(a.away_goals_conceded, 0) as goals_conceded,
        (coalesce(h.home_goals_scored, 0) + coalesce(a.away_goals_scored, 0))
        - (coalesce(h.home_goals_conceded, 0) + coalesce(a.away_goals_conceded, 0)) as goal_difference
    from home_stats h
    full outer join away_stats a on h.team_id = a.team_id
)

select
    c.*,
    t.team_name,
    t.team_short_name,
    t.team_tla,
    t.crest_url,
    t.country,
    t.country_code,
    round(c.goals_scored / nullif(c.total_games, 0), 2) as avg_goals_per_game
from combined c
left join teams t on c.team_id = t.team_id
order by total_wins desc, goal_difference desc
