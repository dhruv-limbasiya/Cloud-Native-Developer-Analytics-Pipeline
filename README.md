# Cloud-Native Developer Analytics Pipeline

A production-inspired Data Engineering project that ingests GitHub organization data using the GitHub REST API, stores raw data in an Amazon S3 data lake following the Medallion Architecture (Bronze → Silver → Gold), performs data quality validation, generates analytical datasets, loads them into PostgreSQL, and visualizes business insights with Power BI.

This project demonstrates how modern Data Engineering pipelines are designed using cloud services, modular ETL architecture, and analytics-ready data models.

---

## Architecture

```text
                     GitHub REST API
                            │
                            ▼
                     AWS Lambda (Extract)
                            │
                            ▼
                    Amazon S3 Bronze Layer
                  (Raw JSON, Partitioned Data)
                            │
                            ▼
                 Bronze → Silver Transformation
                  (Cleaning & Standardization)
                            │
                            ▼
                    Amazon S3 Silver Layer
                     (Clean Parquet Dataset)
                            │
                 Data Quality Validation
                            │
                            ▼
                  Silver → Gold Transformation
                  (Business Analytics Tables)
                            │
                            ▼
                     Amazon S3 Gold Layer
                  (Analytics-ready Parquet)
                            │
                            ▼
                       PostgreSQL Warehouse
                            │
                            ▼
                    Power BI Dashboard
```

---

# Business Problem

Software organizations manage hundreds of repositories and thousands of contributors across GitHub.

Engineering managers often struggle to answer questions such as:

- Which repositories are the most active?
- Which repositories receive the most contributions?
- Which programming languages are most commonly used?
- Which contributors are the most active?
- What is the overall health of the organization?
- How many commits, pull requests, and issues exist across repositories?

This project builds an automated analytics pipeline that collects GitHub data and transforms it into business-ready datasets for reporting and visualization.

---

# Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python 3 |
| Cloud | AWS Lambda, Amazon S3 |
| API | GitHub REST API |
| Data Lake | Amazon S3 |
| Storage Format | JSON, Parquet |
| Data Processing | Pandas |
| Data Validation | Custom Data Quality Framework |
| Database | PostgreSQL |
| Analytics | SQL |
| Visualization | Power BI |
| Configuration | YAML |
| Logging | Python Logging |
| Version Control | Git & GitHub |

---

# Project Structure

```text
developer-analytics-pipeline/

│
├── config/
│   └── config.yaml
│
├── data/
│   ├── bronze/
│   ├── silver/
│   ├── gold/
│   └── metadata/
│
├── logs/
│
├── sql/
│
├── src/
│   ├── extract/
│   ├── storage/
│   ├── bronze/
│   ├── silver/
│   ├── gold/
│   ├── quality/
│   ├── postgres/
│
├── main.py
├── requirements.txt
└── README.md
```

---

# Pipeline Workflow

## Step 1 — Data Extraction

GitHub REST API is used to collect:

- Repositories
- Languages
- Contributors
- Commits
- Issues
- Pull Requests

Extraction is configurable through `config.yaml`.

---

## Step 2 — Bronze Layer

Raw API responses are stored in Amazon S3.

Features

- Raw JSON
- Partitioned by date
- Immutable storage
- Metadata generation
- Incremental ingestion

Example

```
bronze/
    organization=tensorflow/
        endpoint=repositories/
            year=2026/
                month=07/
                    day=24/
```

---

## Step 3 — Silver Layer

Raw JSON files are transformed into standardized datasets.

Operations include

- Schema normalization
- Data cleaning
- Null handling
- Type conversion
- Flattening nested JSON
- Parquet conversion

Output:

- repositories.parquet
- contributors.parquet
- commits.parquet
- languages.parquet
- issues.parquet
- pull_requests.parquet

---

## Step 4 — Data Quality Validation

Each Silver dataset is validated before analytics generation.

Validation includes

- Required columns
- Duplicate detection
- Empty dataset validation
- Null value checks
- Schema consistency

Only validated datasets continue to the Gold layer.

---

## Step 5 — Gold Layer

Business-ready analytical datasets are created.

Generated tables include:

- repository_metrics
- contributor_metrics
- language_metrics
- repository_activity
- organization_summary

These datasets are optimized for reporting and dashboarding.

---

## Step 6 — PostgreSQL Warehouse

Gold datasets are automatically loaded into PostgreSQL.

Benefits

- SQL analytics
- BI integration
- Reporting
- Fast querying

---

## Step 7 — Power BI Dashboard

Power BI connects directly to PostgreSQL to provide interactive dashboards.

Example dashboards

- Repository Overview
- Repository Activity
- Language Distribution
- Top Contributors
- Organization Summary

---

# Configuration

The pipeline is fully configurable.

Example:

```yaml
github:
  organization: tensorflow
  max_repositories: 45
```

Changing the organization or repository limit requires only updating the configuration file.

No code changes are required.

---

# Key Features

- Cloud-native architecture
- Modular ETL pipeline
- Medallion Architecture
- Configurable pipeline
- Incremental ingestion
- Data quality validation
- Metadata tracking
- Analytics-ready datasets
- PostgreSQL integration
- Power BI reporting
- Production-style project structure

---

# Analytics Generated

The project provides insights such as:

- Top repositories by stars
- Repository activity
- Commit statistics
- Pull request activity
- Issue statistics
- Top contributors
- Language usage
- Organization summary
- Repository growth metrics

---

# Skills Demonstrated

- REST API Integration
- Cloud Data Engineering
- Amazon S3
- AWS Lambda
- ETL Pipeline Development
- Data Lake Design
- Medallion Architecture
- Data Validation
- Metadata Management
- PostgreSQL
- SQL Analytics
- Power BI
- Python
- Pandas
- Modular Software Design
- Configuration-driven Development

---

# Future Enhancements

- Apache Airflow orchestration
- AWS Glue Data Catalog
- Amazon Athena
- Apache Spark
- Apache Iceberg
- Great Expectations
- CI/CD using GitHub Actions
- Infrastructure as Code (Terraform)

---

# Learning Outcomes

This project demonstrates the complete lifecycle of a modern cloud-based analytics platform:

- Data ingestion from external APIs
- Cloud object storage
- Layered data architecture
- Data quality validation
- Business transformation
- Relational data warehousing
- Business intelligence reporting

The architecture closely follows real-world data engineering practices used in modern analytics platforms.

---

# Author

**Dhruv Limbasiya**

MCA Student | Aspiring Data Engineer

---