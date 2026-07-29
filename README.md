<p align="center">
  <h1 align="center">☁️ Cloud-Native Developer Analytics Pipeline</h1>
  <p align="center">
    A production-grade data engineering platform that ingests GitHub organization data via the REST API, stores it in an Amazon S3 data lake following the <strong>Medallion Architecture</strong> (Bronze → Silver → Gold), enforces data quality validation, generates analytical datasets, loads them into PostgreSQL, and visualizes business insights with Power BI.
  </p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/AWS_Lambda-FF9900?style=for-the-badge&logo=awslambda&logoColor=white" alt="AWS Lambda">
  <img src="https://img.shields.io/badge/Amazon_S3-569A31?style=for-the-badge&logo=amazons3&logoColor=white" alt="Amazon S3">
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black" alt="Power BI">
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas">
  <img src="https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white" alt="GitHub Actions">
</p>

---

## 📋 Table of Contents

- [Business Problem](#-business-problem)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Pipeline Workflow](#-pipeline-workflow)
- [Getting Started](#-getting-started)
- [Configuration](#-configuration)
- [Data Quality Framework](#-data-quality-framework)
- [CI/CD & Deployment](#-cicd--deployment)
- [Analytics & Dashboards](#-analytics--dashboards)
- [Key Features](#-key-features)
- [Future Enhancements](#-future-enhancements)
- [Author](#-author)

---

## 🎯 Business Problem

Software organizations manage hundreds of repositories and thousands of contributors across GitHub. Engineering leaders often struggle to answer critical questions:

| Question | Insight Area |
|---|---|
| Which repositories are the most active? | Repository Health |
| Who are the top contributors? | Developer Productivity |
| What languages dominate the organization? | Technology Landscape |
| How many open issues and PRs exist? | Backlog Management |
| What is the commit velocity over time? | Engineering Velocity |
| Is the organization growing or stagnating? | Organizational Health |

This project builds an **automated analytics pipeline** that collects GitHub data and transforms it into business-ready datasets for reporting and visualization — eliminating manual data gathering and enabling data-driven engineering decisions.

---

## 🏗 Architecture

```
                         ┌─────────────────────┐
                         │   GitHub REST API    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     AWS Lambda       │
                         │   (Data Extraction)  │
                         └──────────┬──────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
            ┌──────────┐    ┌──────────┐    ┌──────────┐
            │  Bronze   │    │  Silver  │    │   Gold   │
            │  (Raw     │───▶│  (Clean  │───▶│ (Business│
            │   JSON)   │    │ Parquet) │    │ Metrics) │
            └──────────┘    └──────────┘    └──────────┘
                                │                 │
                                ▼                 ▼
                    ┌──────────────────┐  ┌──────────────┐
                    │   Data Quality   │  │  PostgreSQL  │
                    │   Validation     │  │  Warehouse   │
                    └──────────────────┘  └──────┬───────┘
                                                 │
                                                 ▼
                                        ┌──────────────┐
                                        │   Power BI   │
                                        │  Dashboard   │
                                        └──────────────┘
```

> **Medallion Architecture** — Data flows through three progressively refined layers: **Bronze** (immutable raw ingestion) → **Silver** (cleaned & validated) → **Gold** (business-ready analytics).

---

## 🛠 Tech Stack

| Category | Technology | Purpose |
|---|---|---|
| **Language** | Python 3.12 | Core pipeline logic |
| **Cloud Compute** | AWS Lambda | Serverless data extraction |
| **Cloud Storage** | Amazon S3 | Data lake (Bronze / Silver / Gold) |
| **API** | GitHub REST API | Primary data source |
| **Data Processing** | Pandas, PyArrow | Transformation & Parquet I/O |
| **Data Validation** | Custom DQ Framework | Schema, null, duplicate, and range checks |
| **Database** | PostgreSQL + SQLAlchemy | Analytical data warehouse |
| **Visualization** | Power BI | Interactive dashboards |
| **CI/CD** | GitHub Actions | Automated Lambda deployment |
| **Configuration** | YAML + dotenv | Externalized settings |
| **Cloud SDK** | Boto3 | S3 and Lambda integration |

---

## 📁 Project Structure

```
Cloud-Native-Developer-Analytics-Pipeline/
│
├── config/
│   └── config.yaml                  # Pipeline configuration (org, endpoints, limits)
│
├── data/
│   ├── bronze/                      # Raw JSON from GitHub API
│   ├── silver/                      # Cleaned Parquet datasets
│   ├── gold/                        # Business-ready analytics Parquet
│   └── metadata/                    # Ingestion metadata (run tracking)
│
├── docs/
│   ├── api/                         # GitHub API endpoint documentation
│   ├── architecture/                # System design document
│   ├── deployment/                  # Deployment guides
│   ├── diagrams/                    # Architecture diagrams
│   └── screenshots/                 # Dashboard screenshots
│
├── lambda/
│   ├── lambda_handler.py            # AWS Lambda entry point (Bronze pipeline)
│   └── requirements.txt             # Lambda-specific dependencies
│
├── logs/
│   ├── pipeline.log                 # Application log
│   └── dq/                          # Data quality reports (JSON)
│
├── src/
│   ├── core/                        # Shared infrastructure
│   │   ├── config_loader.py         #   YAML configuration loader
│   │   ├── constants.py             #   Global constants (paths, URLs)
│   │   ├── env_loader.py            #   Environment variable loader
│   │   ├── exceptions.py            #   Custom exception classes
│   │   └── logger.py                #   Centralized logging
│   │
│   ├── extract/                     # GitHub API data extraction
│   │   ├── github_client.py         #   HTTP client with retry & pagination
│   │   ├── extractor_factory.py     #   Factory pattern for extractors
│   │   ├── repositories.py          #   Repository extractor
│   │   ├── commits.py               #   Commit extractor
│   │   ├── contributors.py          #   Contributor extractor
│   │   ├── issues.py                #   Issue extractor
│   │   ├── pull_requests.py         #   Pull request extractor
│   │   └── languages.py             #   Language extractor
│   │
│   ├── transform/                   # Bronze → Silver transformations
│   │   ├── base_transformer.py      #   Abstract base with shared logic
│   │   ├── transformer_factory.py   #   Factory pattern for transformers
│   │   ├── repositories_transformer.py
│   │   ├── commits_transformer.py
│   │   ├── contributors_transformer.py
│   │   ├── issues_transformer.py
│   │   ├── pull_requests_transformer.py
│   │   └── languages_transformer.py
│   │
│   ├── dq/                          # Data quality framework
│   │   ├── config.py                #   Per-dataset validation rules
│   │   ├── rules.py                 #   Validation rule implementations
│   │   ├── validator.py             #   Orchestrates validation checks
│   │   ├── gold_validator.py        #   Gold-layer specific validation
│   │   └── report.py                #   DQ report generation & persistence
│   │
│   ├── storage/                     # Read/write abstraction layer
│   │   ├── s3_client.py             #   S3 JSON & Parquet I/O
│   │   ├── bronze_reader.py         #   Read Bronze JSON files
│   │   ├── bronze_writer.py         #   Write Bronze JSON files
│   │   ├── silver_writer.py         #   Write Silver Parquet files
│   │   ├── gold_writer.py           #   Write Gold Parquet files
│   │   ├── parquet_reader.py        #   Generic Parquet reader
│   │   ├── metadata_writer.py       #   Run metadata tracking
│   │   ├── local_storage.py         #   Local filesystem abstraction
│   │   └── file_manager.py          #   File utilities
│   │
│   ├── pipeline/                    # Pipeline orchestration
│   │   ├── bronze/
│   │   │   ├── bronze_pipeline.py   #   Full Bronze ingestion pipeline
│   │   │   └── repository_pipeline.py #  Per-repository extraction
│   │   ├── silver/
│   │   │   └── silver_pipeline.py   #   Bronze → Silver with DQ checks
│   │   └── gold/
│   │       ├── gold_pipeline.py     #   Silver → Gold analytics builder
│   │       ├── repository_metrics.py
│   │       ├── language_metrics.py
│   │       ├── contributor_metrics.py
│   │       ├── repository_activity.py
│   │       └── organization_summary.py
│   │
│   └── serving/                     # Data serving layer
│       ├── db_connection.py         #   PostgreSQL connection via SQLAlchemy
│       ├── postgres_loader.py       #   Gold → PostgreSQL loader
│       └── postgres_writer.py       #   DataFrame-to-table writer
│
├── .github/
│   └── workflows/
│       └── deploy.yml               # CI/CD: Build, test, deploy Lambda
│
├── main.py                          # Local pipeline entry point
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment variable template
├── .gitignore                       # Git exclusions
└── README.md
```

---

## ⚙ Pipeline Workflow

### Step 1 — Data Extraction (Bronze Layer)

The **Bronze Pipeline** runs on AWS Lambda and extracts raw data from the GitHub REST API.

**Data Sources:**

| Endpoint | Data Collected |
|---|---|
| `/orgs/{org}/repos` | Repositories (name, stars, forks, language, dates) |
| `/repos/{owner}/{repo}/languages` | Language byte counts per repository |
| `/repos/{owner}/{repo}/contributors` | Contributors and contribution counts |
| `/repos/{owner}/{repo}/commits` | Commit SHA, author, date, message |
| `/repos/{owner}/{repo}/issues` | Issue number, state, labels, dates |
| `/repos/{owner}/{repo}/pulls` | PR number, state, created/merged dates |

**Features:** Automatic pagination · Configurable retry logic (3 attempts) · Rate-limit awareness · Date-partitioned storage

**Storage Format:**
```
bronze/
  organization=tensorflow/
    endpoint=repositories/
      year=2026/
        month=07/
          day=29/
            repositories.json
```

---

### Step 2 — Data Transformation (Silver Layer)

The **Silver Pipeline** reads Bronze JSON, applies per-dataset transformers, and outputs clean Parquet files.

**Transformations Applied:**
- Schema normalization and column renaming
- Nested JSON flattening
- Datetime parsing (UTC)
- Null value handling
- Column selection (drop unused fields)
- Type casting

**Output Datasets:** `repositories.parquet` · `contributors.parquet` · `commits.parquet` · `languages.parquet` · `issues.parquet` · `pull_requests.parquet`

---

### Step 3 — Data Quality Validation

Every Silver dataset is validated **before** it proceeds to the Gold layer. If any check fails, the pipeline halts immediately.

| Check | Description |
|---|---|
| **Empty Dataset** | Ensures dataset contains at least one row |
| **Required Columns** | Verifies all expected columns are present |
| **Null Values** | Counts nulls in required columns |
| **Duplicate Detection** | Checks for duplicate records on a key column |
| **Negative Values** | Validates numeric columns contain no negatives |

DQ reports are persisted as JSON files under `logs/dq/` for auditability.

---

### Step 4 — Business Analytics (Gold Layer)

The **Gold Pipeline** aggregates Silver datasets into five business-ready analytical tables:

| Gold Dataset | Source Data | Key Metrics |
|---|---|---|
| `repository_metrics` | Repositories | Stars, forks, watchers, repo age |
| `language_metrics` | Languages | Byte count, language distribution |
| `contributor_metrics` | Contributors | Total contributions per user |
| `repository_activity` | Commits + Issues + PRs | Commit count, issue count, PR count per repo |
| `organization_summary` | All Gold datasets | Aggregate org-level KPIs |

---

### Step 5 — Data Serving (PostgreSQL)

Gold Parquet files are automatically loaded into PostgreSQL using SQLAlchemy, making them queryable via standard SQL and connectable to any BI tool.

---

### Step 6 — Visualization (Power BI)

Power BI connects directly to PostgreSQL to provide interactive dashboards:

- **Repository Overview** — Stars, forks, and watchers by repository
- **Repository Activity** — Commits, issues, and PRs over time
- **Language Distribution** — Technology landscape across the organization
- **Top Contributors** — Most active developers
- **Organization Summary** — High-level health metrics

---

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- PostgreSQL 14+
- AWS Account (for S3 and Lambda)
- GitHub Personal Access Token ([create one here](https://github.com/settings/tokens))
- Power BI Desktop (optional, for dashboards)

### 1. Clone the Repository

```bash
git clone https://github.com/dhruv-limbasiya/Cloud-Native-Developer-Analytics-Pipeline.git
cd Cloud-Native-Developer-Analytics-Pipeline
```

### 2. Create a Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
GITHUB_TOKEN=ghp_your_personal_access_token_here
AWS_REGION=us-east-1
```

> ⚠️ **Never commit your `.env` file.** It is already included in `.gitignore`.

### 5. Update Configuration

Edit `config/config.yaml` to set the target GitHub organization and pipeline parameters:

```yaml
github:
  organizations:
    - tensorflow          # Target organization

  organization_endpoints:
    - repositories

  repository_endpoints:
    - languages
    - commits
    - issues
    - pull_requests
    - contributors

  per_page: 100           # Records per API page
  max_repositories: 54    # Limit repositories to process
  request_timeout: 30     # API timeout in seconds
  retry_count: 3          # Retry attempts on failure
  max_pages: 2            # Max pages to paginate

postgres:
  host: localhost
  port: 5432
  database: developer_analytics
  username: postgres
  password: your_password
```

### 6. Set Up PostgreSQL

```sql
CREATE DATABASE developer_analytics;
```

### 7. Run the Pipeline

```bash
python main.py
```

This executes: **Silver Pipeline** → **Gold Pipeline** → **PostgreSQL Loading**

> **Note:** The Bronze pipeline runs separately on AWS Lambda. For local testing, ensure Bronze data exists in `data/bronze/`.

---

## 🔧 Configuration

The pipeline is fully **configuration-driven** — no code changes are needed to analyze a different organization.

| Parameter | Description | Default |
|---|---|---|
| `organizations` | GitHub organization to analyze | `tensorflow` |
| `max_repositories` | Maximum number of repos to process | `54` |
| `per_page` | Records per API page | `100` |
| `max_pages` | Maximum pages to paginate | `2` |
| `request_timeout` | API request timeout (seconds) | `30` |
| `retry_count` | Retry attempts on API failure | `3` |

To switch organizations, simply update `config/config.yaml`:

```yaml
github:
  organizations:
    - google        # or: apache, kubernetes, microsoft, netflix
```

---

## 🛡 Data Quality Framework

The custom-built DQ framework validates every dataset at the Silver layer before promotion to Gold.

```
┌─────────────────────────────────────────┐
│          DataQualityValidator           │
│                                         │
│  ┌─────────┐  ┌────────┐  ┌─────────┐  │
│  │ Rules   │  │ Config │  │ Report  │  │
│  │ Engine  │  │ (YAML) │  │ Writer  │  │
│  └─────────┘  └────────┘  └─────────┘  │
│                                         │
│  Checks: empty · columns · nulls ·     │
│           duplicates · negatives        │
└─────────────────────────────────────────┘
```

**Behavior:** If validation **fails**, the pipeline raises a `ValueError` and stops execution — preventing bad data from reaching the Gold layer or PostgreSQL.

**Reports:** Each validation run generates a JSON report stored at:
```
logs/dq/organization={org}/dataset={name}/year={Y}/month={M}/day={D}/report.json
```

---

## 🔄 CI/CD & Deployment

The project uses **GitHub Actions** for automated CI/CD on every push to `main`:

```yaml
# .github/workflows/deploy.yml
Trigger:     Push to main / master
Runner:      ubuntu-latest
Python:      3.12

Steps:
  1. Checkout repository
  2. Setup Python 3.12
  3. Validate syntax (py_compile)
  4. Install Lambda dependencies → build/
  5. Package source code → deployment.zip
  6. Upload artifact
  7. Configure AWS credentials (from GitHub Secrets)
  8. Deploy to AWS Lambda
```

**Required GitHub Secrets:**

| Secret | Description |
|---|---|
| `AWS_ACCESS_KEY_ID` | AWS IAM access key |
| `AWS_SECRET_ACCESS_KEY` | AWS IAM secret key |
| `AWS_REGION` | AWS region (e.g., `us-east-1`) |
| `LAMBDA_FUNCTION_NAME` | Lambda function name |

---

## 📊 Analytics & Dashboards

### Generated Insights

| Metric | Description |
|---|---|
| **Top Repositories** | Ranked by stars, forks, and watchers |
| **Repository Activity** | Commits, issues, and PRs per repository |
| **Commit Statistics** | Commit frequency and author analysis |
| **Pull Request Activity** | PR volume, state distribution |
| **Issue Statistics** | Open vs. closed issues, backlog size |
| **Top Contributors** | Most active developers by contributions |
| **Language Distribution** | Byte count and percentage by language |
| **Organization Summary** | Aggregate KPIs across all repositories |

---

## ✨ Key Features

| Feature | Description |
|---|---|
| **Medallion Architecture** | Three-layer data lake (Bronze → Silver → Gold) |
| **Serverless Extraction** | AWS Lambda for scheduled, event-driven ingestion |
| **Configuration-Driven** | Change organization or limits via YAML — zero code changes |
| **Data Quality Gates** | Automated validation prevents bad data propagation |
| **Factory Pattern** | Pluggable extractors and transformers for each endpoint |
| **Automatic Pagination** | Handles multi-page API responses transparently |
| **Retry with Backoff** | Resilient HTTP client with configurable retries |
| **Rate-Limit Awareness** | Logs remaining API quota from response headers |
| **Metadata Tracking** | Every pipeline run logs status, record count, and file path |
| **Partitioned Storage** | Data organized by `organization/endpoint/year/month/day` |
| **CI/CD Pipeline** | GitHub Actions builds, validates, and deploys Lambda automatically |
| **DQ Reporting** | JSON audit trail for every validation run |

---

## 🔮 Future Enhancements

- [ ] Apache Airflow orchestration
- [ ] AWS Glue Data Catalog integration
- [ ] Amazon Athena for serverless SQL
- [ ] Apache Spark for large-scale processing
- [ ] Apache Iceberg table format
- [ ] Great Expectations for advanced data validation
- [ ] Infrastructure as Code with Terraform
- [ ] Multi-organization support
- [ ] GitHub GraphQL API migration
- [ ] Real-time streaming with Kafka

---

## 📄 Documentation

| Document | Description |
|---|---|
| [System Design](docs/architecture/system_design.md) | Detailed architecture and design decisions |
| [GitHub API Endpoints](docs/api/github_endpoints.md) | API endpoint reference and data schema |

---

## 👤 Author

**Dhruv Limbasiya**

MCA Student · Aspiring Data Engineer

[![GitHub](https://img.shields.io/badge/GitHub-dhruv--limbasiya-181717?style=flat&logo=github)](https://github.com/dhruv-limbasiya)

---

<p align="center">
  <sub>Built with ❤️ as a production-inspired Data Engineering portfolio project.</sub>
</p>