# Pipeline Flow

## Overview

The GitHub Engineering Intelligence Platform follows a Medallion Architecture to transform raw GitHub API data into analytics-ready datasets.

```
GitHub REST API
        │
        ▼
AWS Lambda (Extract)
        │
        ▼
S3 Bronze (JSON)
        │
        ▼
Bronze → Silver ETL
        │
        ▼
S3 Silver (Parquet)
        │
        ▼
Data Quality Validation
        │
        ▼
Silver → Gold ETL
        │
        ▼
S3 Gold (Parquet)
        │
        ▼
DuckDB
        │
        ▼
Power BI / Superset
```

---

# Pipeline Execution

The complete pipeline executes in the following order.

1. EventBridge triggers the workflow.
2. Step Functions starts the pipeline.
3. Lambda extracts GitHub data.
4. Raw JSON is stored in Bronze.
5. Bronze data is transformed into Silver.
6. Data Quality validation runs.
7. Silver is transformed into Gold.
8. Gold datasets are queried using DuckDB.
9. Dashboards are refreshed.
10. SNS sends success or failure notifications.

---

# Step 1 — Extraction

Input

- GitHub REST API

Process

- Authenticate
- Read configuration
- Fetch repositories
- Fetch commits
- Fetch pull requests
- Fetch issues
- Fetch contributors
- Fetch languages
- Handle pagination
- Retry failed requests
- Handle rate limits

Output

Raw JSON

---

# Step 2 — Bronze Layer

Purpose

Store immutable API responses.

Format

JSON

Example

```
bronze/

endpoint=repositories/

year=2026/

month=07/

day=17/

repositories.json
```

No transformation occurs.

---

# Step 3 — Bronze to Silver

Purpose

Convert raw API data into standardized datasets.

Transformations

- Flatten nested JSON
- Standardize column names
- Remove duplicates
- Handle missing values
- Convert timestamps
- Add ingestion timestamp
- Convert JSON to Parquet

Output

Silver Parquet datasets.

---

# Step 4 — Data Quality

Validation Rules

- Schema validation
- Duplicate validation
- Null validation
- Empty dataset validation
- Freshness validation
- Business rule validation

If validation fails

- Stop pipeline
- Send SNS notification
- Do not create Gold datasets

---

# Step 5 — Silver to Gold

Purpose

Create analytics-ready datasets.

Generated tables

- repository_activity
- developer_activity
- issue_metrics
- pull_request_metrics
- language_distribution
- repository_growth
- engineering_productivity

---

# Step 6 — Analytics

DuckDB reads Gold datasets.

Example analyses

- Top repositories
- Repository growth
- Active contributors
- Pull request trends
- Language distribution
- Engineering productivity

---

# Step 7 — Dashboard

Visualization tool

- Power BI
- Apache Superset

Dashboard Pages

- Repository Overview
- Developer Overview
- Pull Request Analytics
- Issue Analytics
- Technology Distribution
- Engineering Productivity

---

# Automation

```
EventBridge

↓

Step Functions

↓

Lambda

↓

Bronze

↓

Silver ETL

↓

Data Quality

↓

Gold ETL

↓

Notification
```

---

# Failure Handling

Extraction Failure

↓

Retry

↓

SNS Alert

Transformation Failure

↓

Stop Pipeline

↓

SNS Alert

Data Quality Failure

↓

Stop Pipeline

↓

SNS Alert

---

# Monitoring

CloudWatch monitors

- Lambda duration
- Lambda errors
- API failures
- Pipeline duration
- Data Quality failures

---

# Logging

Each pipeline execution records

- Run ID
- Execution time
- Organization
- Endpoint
- Records extracted
- Status
- Error message