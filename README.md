# Cloud-Native Developer Analytics Pipeline

> A cloud-native Data Engineering project that extracts GitHub organization data, processes it using a Medallion Architecture, validates data quality, and generates analytics-ready datasets for business intelligence.

---

## Project Overview

The **Cloud-Native Developer Analytics Pipeline** is an end-to-end Data Engineering project designed to demonstrate modern data engineering practices using GitHub engineering data.

The pipeline automatically collects data from the GitHub REST API, stores immutable raw data, transforms it into analytics-ready datasets, validates data quality, and prepares business metrics for reporting and visualization.

This project follows industry-standard architecture including:

- Medallion Architecture (Bronze → Silver → Gold)
- Configuration-driven pipeline
- Modular ETL design
- Data Quality Validation
- Cloud storage integration
- Analytics-ready datasets

---

## Business Problem

Engineering managers and technical leaders often need answers to questions such as:

- Which repositories are most active?
- Which developers contribute the most?
- How quickly are pull requests merged?
- How many issues remain unresolved?
- Which programming languages are most used?
- How is repository activity changing over time?

Instead of manually collecting this information, this project automates the complete analytics pipeline.

---

## Architecture

```
                    GitHub REST API
                           │
                           ▼
                    Data Extraction
                           │
                           ▼
                 Bronze Layer (JSON)
                           │
                           ▼
                  Bronze → Silver ETL
                           │
                           ▼
                Silver Layer (Parquet)
                           │
                           ▼
                Data Quality Validation
                           │
                           ▼
                  Silver → Gold ETL
                           │
                           ▼
                 Gold Layer (Parquet)
                           │
                           ▼
                       DuckDB
                           │
                           ▼
              Power BI / Apache Superset
```

---

## Medallion Architecture

### Bronze Layer

Purpose

- Store raw GitHub API responses
- Immutable data
- JSON format
- Source of truth

---

### Silver Layer

Purpose

- Clean and standardize data
- Remove duplicates
- Handle null values
- Normalize schema
- Convert JSON to Parquet

---

### Gold Layer

Purpose

Generate business-ready datasets for analytics including:

- Repository Analytics
- Developer Analytics
- Pull Request Metrics
- Issue Metrics
- Language Distribution
- Engineering Productivity
- Repository Growth

---

## Project Structure

```
cloud-native-developer-analytics-pipeline/

├── config/
│   └── config.yaml
│
├── data/
│   ├── bronze/
│   ├── silver/
│   ├── gold/
│   └── metadata/
│
├── docs/
│   ├── api/
│   ├── architecture/
│   ├── deployment/
│   ├── diagrams/
│   └── screenshots/
│
├── logs/
│
├── src/
│   ├── core/
│   ├── dq/
│   ├── extract/
│   ├── storage/
│   ├── transform/
│   └── utils/
│
├── tests/
│
├── main.py
├── requirements.txt
├── README.md
└── .env.example
```

---

## Features

- GitHub REST API Integration
- Configuration Driven Design
- Modular ETL Pipeline
- Medallion Architecture
- Data Quality Validation
- Structured Logging
- Incremental Data Loading
- Local Development Support
- Cloud Storage Ready
- Analytics Ready Outputs

---

## Technology Stack

| Category | Technology |
|----------|------------|
| Language | Python |
| Cloud | AWS |
| Storage | Amazon S3 |
| API | GitHub REST API |
| Data Format | JSON, Parquet |
| Data Processing | Pandas |
| Analytics | DuckDB |
| Dashboard | Power BI / Apache Superset |
| Configuration | YAML |
| Logging | Python Logging |
| Version Control | Git & GitHub |

---

## Pipeline Flow

1. Read configuration
2. Authenticate with GitHub
3. Extract organization data
4. Store raw JSON in Bronze
5. Transform Bronze → Silver
6. Execute Data Quality Validation
7. Transform Silver → Gold
8. Query Gold datasets using DuckDB
9. Visualize metrics in BI tools

---

## GitHub Data Sources

The pipeline extracts data from:

- Organization
- Repositories
- Contributors
- Commits
- Pull Requests
- Issues
- Languages

---

## Data Quality Checks

The pipeline validates:

- Schema consistency
- Duplicate records
- Missing values
- Empty datasets
- Data freshness
- Business rules

Failed validation prevents Gold datasets from being generated.

---

## Configuration

The pipeline is fully configuration driven.

Example:

```yaml
github:
  organizations:
    - tensorflow
```

Changing the organization requires no code modification.

---

## Logging

The pipeline records:

- Pipeline execution
- API requests
- Records processed
- Transformation status
- Validation results
- Errors
- Execution duration

---

## Future Enhancements

- AWS Lambda
- Step Functions
- EventBridge Scheduling
- CloudWatch Monitoring
- SNS Notifications
- Athena
- Glue Catalog
- CI/CD with GitHub Actions
- Infrastructure as Code (CloudFormation/Terraform)

---

## Current Project Status

| Module | Status |
|---------|--------|
| Project Structure | Completed |
| Configuration | Completed |
| Documentation | Completed |
| Logging | Completed |
| GitHub API Client | In Progress |
| Bronze Layer | Planned |
| Silver Layer | Planned |
| Gold Layer | Planned |
| Data Quality | Planned |
| Analytics | Planned |
| Dashboard | Planned |
| AWS Deployment | Planned |

---

## Learning Objectives

This project demonstrates practical experience with:

- Data Engineering Fundamentals
- ETL Pipeline Design
- Cloud Data Storage
- Medallion Architecture
- REST API Integration
- Data Validation
- Analytics Engineering
- Modular Python Development
- Production-ready Project Organization

---

## License

This project is developed for educational and portfolio purposes.