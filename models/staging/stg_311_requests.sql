with source as (
    select * from {{ source('nyc311', '311_service_requests') }}
),

renamed as (
    select
        unique_key,
        created_date,
        closed_date,
        agency,
        agency_name,
        complaint_type,
        descriptor,
        location_type,
        borough,
        city,
        latitude,
        longitude,
        status,

        -- computed fields
        TIMESTAMP_DIFF(closed_date, created_date, HOUR) as response_hours

    from source
    where borough != 'Unspecified'
      and borough is not null
      and created_date is not null
)

select * from renamed