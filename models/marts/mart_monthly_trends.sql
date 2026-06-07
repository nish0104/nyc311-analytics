with enriched as (
    select * from {{ ref('int_agency_sla_flags') }}
)

select
    year_month,
    request_year,
    request_month,
    complaint_type,
    borough,
    COUNT(*)                                                    as total_requests,
    ROUND(AVG(response_hours), 1)                              as avg_response_hours,
    ROUND(COUNTIF(sla_status = 'On Time') / COUNT(*) * 100, 1) as sla_compliance_pct

from enriched
group by year_month, request_year, request_month, complaint_type, borough
order by year_month