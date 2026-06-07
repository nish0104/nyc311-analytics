with stg as (
    select * from {{ ref('stg_311_requests') }}
)

select
    unique_key,
    created_date,
    closed_date,
    agency,
    agency_name,
    complaint_type,
    descriptor,
    borough,
    status,
    latitude,
    longitude,
    response_hours,

    -- time dimensions
    EXTRACT(YEAR FROM created_date)  as request_year,
    EXTRACT(MONTH FROM created_date) as request_month,
    EXTRACT(HOUR FROM created_date)  as request_hour,
    FORMAT_DATE('%A', DATE(created_date)) as day_of_week,
    FORMAT_DATE('%Y-%m', DATE(created_date)) as year_month

from stg