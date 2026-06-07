with sla as (
    select * from {{ ref('int_agency_sla_flags') }}
)

select
    agency_name,
    COUNT(*)                                                    as total_requests,
    ROUND(AVG(response_hours), 1)                              as avg_response_hours,
    COUNTIF(sla_status = 'On Time')                            as on_time_count,
    COUNTIF(sla_status = 'Overdue')                            as overdue_count,
    COUNTIF(sla_status = 'Open')                               as open_count,
    ROUND(COUNTIF(sla_status = 'On Time') / COUNT(*) * 100, 1) as sla_compliance_pct

from sla
group by agency_name
order by total_requests desc
