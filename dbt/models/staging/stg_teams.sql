with source as (
    select * from {{ source('mundial_raw', 'teams') }}
),

renamed as (
    select
        id                  as team_id,
        name                as team_name,
        shortName           as team_short_name,
        tla                 as team_tla,
        crestUrl            as crest_url,
        area.name           as country,
        area.code           as country_code,
        founded,
        venue
    from source
)

select * from renamed
