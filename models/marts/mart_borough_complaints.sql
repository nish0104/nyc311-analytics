with sla as (
    select * from {{ ref('int_agency_sla_flags') }}
)

select
    borough,
    complaint_type,
    COUNT(*)                                                    as total_requests,
    ROUND(AVG(response_hours), 1)                              as avg_response_hours,
    ROUND(COUNTIF(sla_status = 'On Time') / COUNT(*) * 100, 1) as sla_compliance_pct

from sla
group by borough, complaint_type
order by borough, total_requests desc