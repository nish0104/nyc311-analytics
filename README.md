\# 🗽 NYC 311 Service Request Analytics



> End-to-end analytics engineering project · dbt Core + BigQuery + Streamlit



!\[Python](https://img.shields.io/badge/Python-3.13-blue)

!\[dbt](https://img.shields.io/badge/dbt-1.11-orange)

!\[BigQuery](https://img.shields.io/badge/BigQuery-GCP-blue)

!\[Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)



\## 📌 Project Overview



An end-to-end analytics engineering pipeline that ingests 25M+ real NYC 311 service requests from BigQuery public data, models them through a three-layer dbt architecture (Staging → Intermediate → Marts), and serves insights through an interactive Streamlit dashboard.



\*\*Business Questions Answered:\*\*

\- Which NYC agencies have the worst 311 response times?

\- Which boroughs generate the most complaints — and what types?

\- How has city responsiveness changed from 2010 to present?

\- Which agencies consistently miss their 24-hour SLA?



\## 🏗️ Architecture



bigquery-public-data.new\_york\_311

↓

stg\_311\_requests        ← Staging: clean, cast, filter

↓

int\_requests\_enriched   ← Intermediate: time dimensions

↓

int\_agency\_sla\_flags    ← Intermediate: SLA classification

↓

┌─────────────────────────────────────┐

│ mart\_agency\_performance             │

│ mart\_borough\_complaints             │  ← Marts: aggregated tables

│ mart\_monthly\_trends                 │

└─────────────────────────────────────┘

↓

Streamlit Dashboard (4 pages)



\## 🛠️ Tech Stack



| Layer | Tool |

|-------|------|

| Cloud Warehouse | BigQuery (GCP) |

| Transformation | dbt Core 1.11 |

| Orchestration | dbt build (dependency-aware) |

| Dashboard | Streamlit + Plotly |

| Language | Python 3.13, SQL |

| Version Control | GitHub |



\## 📊 Dashboard Pages



1\. \*\*Executive Summary\*\* — KPI cards (25.7M requests, avg response time, SLA %), top 10 agencies by volume

2\. \*\*Agency Performance Scorecard\*\* — scatter plot of response time vs SLA compliance, bottom 10 agencies table

3\. \*\*Borough Analysis\*\* — complaint volume by borough, top complaint types with interactive filter

4\. \*\*Trend Analysis\*\* — monthly trends by complaint type (2010–present), day-of-week × hour heatmap



\## 🗂️ dbt Model Structure

models/

├── staging/

│   ├── sources.yml              # BigQuery public data source definition

│   ├── schema.yml               # Column descriptions + 7 data quality tests

│   └── stg\_311\_requests.sql     # Clean, cast, filter source data

├── intermediate/

│   ├── int\_requests\_enriched.sql  # Add time dimensions (year, month, hour, day)

│   └── int\_agency\_sla\_flags.sql   # Classify requests: On Time / Overdue / Open

└── marts/

├── mart\_agency\_performance.sql  # Aggregated agency SLA metrics

├── mart\_borough\_complaints.sql  # Complaint breakdown by borough

└── mart\_monthly\_trends.sql      # Time-series request volume



\## ✅ Data Quality



7 automated dbt tests on the staging layer:

\- `unique` + `not\_null` on `unique\_key`

\- `not\_null` on `created\_date`, `agency\_name`, `complaint\_type`

\- `not\_null` + `accepted\_values` on `borough`

\- Negative response hours filtered at source


## 🌐 Live Dashboard

👉 [View Live Dashboard](https://nyc311-dashboard-675082933231.us-central1.run.app)



\## 🚀 How to Run Locally



\### Prerequisites

\- Python 3.10+

\- Google Cloud account with BigQuery access

\- gcloud CLI installed and authenticated



\### Setup



```bash

\# Clone the repo

git clone https://github.com/nish0104/nyc311-analytics.git

cd nyc311-analytics



\# Install dependencies

pip install dbt-core dbt-bigquery streamlit plotly pandas google-cloud-bigquery db-dtypes



\# Authenticate with GCP

gcloud auth application-default login



\# Configure dbt profile (edit \~/.dbt/profiles.yml with your project ID)



\# Run dbt pipeline

dbt debug        # verify connection

dbt run          # build all models

dbt test         # run data quality tests

dbt docs serve   # view lineage DAG



\# Launch dashboard

streamlit run dashboard.py

```



\## 📸 Screenshots



\### Lineage DAG

!\[Lineage DAG](assets/lineage\_dag.png)



\### Executive Summary

!\[Executive Summary](assets/dashboard\_executive.png)



\### Agency Performance

!\[Agency Performance](assets/dashboard\_agency.png)



\### Borough Analysis

!\[Borough Analysis](assets/dashboard\_borough.png)



\### Trend Analysis

!\[Trend Analysis](assets/dashboard\_trends.png)



\## 🔑 Key Design Decisions



\*\*Why dbt on BigQuery vs local DuckDB?\*\*

Previous projects used dbt with DuckDB locally. This project targets the production analytics engineering stack — BigQuery's columnar engine processing 1.6 GiB per query, with GCP IAM, cloud-managed infrastructure, and dbt's full three-layer architecture.



\*\*Why NYC 311?\*\*

30M+ rows of real civic data with rich temporal and geographic dimensions — ideal for demonstrating aggregation patterns, SLA analytics, and time-series modeling at scale.



\## 👩‍💻 Author



\*\*Nishthaben Vaghani\*\* · \[GitHub](https://github.com/nish0104) · \[LinkedIn](https://linkedin.com/in/your-linkedin)

