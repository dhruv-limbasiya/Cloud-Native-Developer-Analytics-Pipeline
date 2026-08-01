# Cloud-Native Developer Analytics Platform — Architecture Diagrams

This directory contains visual architecture diagrams and sequence flows for the platform.

---

## 1. High-Level Architecture Flow

```
  ┌─────────────────┐
  │   GitHub API    │  (Telemetry Extraction)
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │   AWS Lambda    │  (Serverless Ingestion Engine)
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │ S3 Bronze Layer │  (Raw JSON / Parquet Data Lake)
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │ S3 Silver Layer │  (Standardized & Cleaned Schemas)
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │  S3 Gold Layer  │  (Aggregated Business Metrics)
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │   PostgreSQL    │  (Relational Serving Database)
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │    Streamlit    │  (6-Page Interactive BI Dashboard)
  └─────────────────┘
```

---

## 2. Medallion Pipeline Sequence Diagram

```mermaid
sequenceDiagram
    autonumber
    participant GH as GitHub API
    participant L as AWS Lambda
    participant B as S3 Bronze
    participant S as S3 Silver
    participant G as S3 Gold
    participant DB as PostgreSQL
    participant UI as Streamlit Dashboard

    GH->>L: Fetch repo, language, commit, issue & contributor telemetry
    L->>B: Save raw extracted Parquet files (Bronze)
    B->>S: Run schema casting & null validation (Silver)
    S->>G: Compute metrics & aggregations (Gold)
    G->>DB: Load Gold datasets via SQLAlchemy (PostgresLoader)
    DB->>UI: Serve cached queries (@st.cache_data) to 6 dashboard pages
```
