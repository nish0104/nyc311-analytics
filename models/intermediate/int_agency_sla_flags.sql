with enriched as (
    select * from {{ ref('int_requests_enriched') }}
)

select
    *,
    case
        when response_hours is null then 'Open'
        when response_hours <= 24   then 'On Time'
        when response_hours > 24    then 'Overdue'
    end as sla_status

from enriched