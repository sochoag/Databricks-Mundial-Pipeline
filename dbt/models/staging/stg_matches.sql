with source as (
    select * from {{ source('mundial_raw', 'matches') }}
),

renamed as (
    select
        id                                          as match_id,
        utcDate                                     as match_date,
        status,
        matchday,
        stage,
        homeTeam.id                                 as home_team_id,
        homeTeam.name                               as home_team_name,
        homeTeam.crestUrl                           as home_team_crest,
        awayTeam.id                                 as away_team_id,
        awayTeam.name                               as away_team_name,
        awayTeam.crestUrl                           as away_team_crest,
        score.fullTime.home                         as home_goals,
        score.fullTime.away                         as away_goals,
        score.winner                                as winner,
        score.duration                              as duration
    from source
    where status = 'FINISHED'
)

select * from renamed
