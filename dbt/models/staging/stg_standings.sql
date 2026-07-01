with source as (
    select * from {{ source('mundial_raw', 'standings') }}
),

renamed as (
    select
        stage,
        type,
        group                       as group_name,
        table_entry.position        as position,
        table_entry.team.id         as team_id,
        table_entry.team.name       as team_name,
        table_entry.playedGames     as played_games,
        table_entry.won             as won,
        table_entry.draw            as draw,
        table_entry.lost            as lost,
        table_entry.points          as points,
        table_entry.goalsFor        as goals_for,
        table_entry.goalsAgainst    as goals_against,
        table_entry.goalDifference  as goal_difference
    from source,
    lateral flatten(input => table) as table_entry
)

select * from renamed
