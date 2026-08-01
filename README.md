<p align="center">
  <h1 align="center">⚡ Cloud-Native Developer Analytics Platform</h1>
  <p align="center">
    An end-to-end data engineering platform that extracts GitHub organization telemetry via REST API, processes it through an S3 Data Lake (Bronze → Silver → Gold), validates data quality, serves analytical models in PostgreSQL, and powers an interactive 6-page Streamlit analytics dashboard.
  </p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/AWS_Lambda-FF9900?style=for-the-badge&logo=awslambda&logoColor=white" alt="AWS Lambda">
  <img src="https://img.shields.io/badge/Amazon_S3-569A31?style=for-the-badge&logo=amazons3&logoColor=white" alt="Amazon S3">
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white" alt="Plotly">
  <img src="https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white" alt="GitHub Actions">
</p>

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Architecture](#-architecture)
- [Medallion Data Lake Design](#-medallion-data-lake-design)
- [Interactive Streamlit Dashboard](#-interactive-streamlit-dashboard)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Data Quality & Metadata](#-data-quality--metadata)
- [CI/CD & Deployment](#-cicd--deployment)
- [How to Run](#-how-to-run)
- [Resume Summary](#-resume-summary)

---

## 🚀 Overview

Engineering leaders managing large GitHub organizations (such as `tensorflow`) often lack centralized visibility into repository growth, code volume distribution, contributor engagement, and issue backlog velocity.

This project delivers an automated, cloud-native data engineering pipeline that continuously extracts, transforms, and serves developer telemetry.

### Key Value Delivered
- **Automated Telemetry Extraction**: Collects repository metadata, language breakdowns, commit histories, contributor metrics, issue counts, and pull requests via GitHub REST API.
- **Medallion Data Lake**: Implements Bronze (raw JSON/Parquet), Silver (cleaned/standardized), and Gold (aggregated business metrics) partitions in Apache Parquet format.
- **Serving Layer**: Automatically loads Gold analytics datasets into PostgreSQL via SQLAlchemy.
- **Executive BI Dashboard**: A 6-page interactive Streamlit dashboard providing executive insights, top repository rankings, language distributions, contributor leaderboards, and activity metrics.

---

## 🏗️ Architecture

```
                                  CLOUD DATA PIPELINE ARCHITECTURE
                                  
  ┌───────────────┐        ┌──────────────┐        ┌────────────────┐        ┌────────────────┐
  │  GitHub API   │ ────>  │  AWS Lambda  │ ────>  │ S3 Data Lake   │ ────>  │ Silver Layer   │
  │  (Telemetry)  │        │ (Extraction) │        │ (Bronze Layer) │        │ (Standardized) │
  └───────────────┘        └──────────────┘        └────────────────┘        └────────────────┘
                                                                                      │
  ┌───────────────┐        ┌──────────────┐        ┌────────────────┐                 │
  │   Streamlit   │ <────  │  PostgreSQL  │ <────  │   Gold Layer   │ <────────────────┘
  │  (Dashboard)  │        │ (Database)   │        │ (Aggregated)   │
  └───────────────┘        └──────────────┘        └────────────────┘
```

### Data Pipeline Sequence
1. **Extraction (Bronze)**: AWS Lambda fetches raw telemetry from GitHub API endpoints and writes partitioned Parquet files to `data/bronze/`.
2. **Standardization (Silver)**: PyArrow/Pandas cleans, casts data types, handles null values, and writes standardized schema files to `data/silver/`.
3. **Aggregation (Gold)**: Summarizes repository metrics, language bytes, contributor stats, and activity totals in `data/gold/`.
4. **Serving Layer**: `PostgresLoader` loads Gold datasets into relational PostgreSQL tables.
5. **Analytics Dashboard**: Streamlit queries PostgreSQL using SQLAlchemy with `@st.cache_data` caching to power 6 analytical views.

---

## 🥇 Medallion Data Lake Design

| Partition Layer | Format | Path | Purpose |
|---|---|---|---|
| **Bronze Layer** | Parquet | `data/bronze/organization={org}/dataset={name}/` | Raw ingestion preserves original API responses |
| **Silver Layer** | Parquet | `data/silver/organization={org}/dataset={name}/` | Cleaned schema, formatted datetimes, null handling |
| **Gold Layer** | Parquet | `data/gold/organization={org}/dataset={name}/` | Aggregated business metrics ready for BI |
| **PostgreSQL** | Relational | `developer_analytics` database | Queryable serving layer for web dashboards & SQL analytics |

---

## 📊 Interactive Streamlit Dashboard

The platform includes a modern 6-page BI dashboard built with Streamlit, Plotly, and custom GitHub-inspired CSS styling (`#f6f8fa` clean white theme, rounded cards, subtle shadows).

### 1. 🏠 Executive Overview
Includes a pipeline flow architecture visual, 7 high-level KPI cards, top 10 repos by stars/forks, language distribution donut chart, top contributors, and factual activity breakdown.

![Home Page Dashboard](docs/images/dashboard_home.png)

### 2. 📦 Repository Analytics
Features top repo bar charts, Watchers vs. Stars scatter plot (sized by forks, colored by language), repository size analysis, and a searchable statistics data table.

![Repository Analytics Page](docs/images/dashboard_repository.png)

### 3. 👥 Contributor Analytics
Displays top contributing repositories, contributor count breakdown, contributions distribution histogram, and a ranked contributor leaderboard.

![Contributor Analytics Page](docs/images/dashboard_contributor.png)

### 4. 💻 Language Analytics
Highlights language distribution donut chart, code volume by language bar chart, and language statistics table with percentage volume badges.

![Language Analytics Page](docs/images/dashboard_language.png)

### 5. 📊 Activity Analytics
Provides side-by-side Commit, Issue, and Pull Request bar charts per repository along with an activity table.

![Activity Analytics Page](docs/images/dashboard_activity.png)

### 6. 🏢 Organization Summary
Presents high-level organization KPI cards and an executive summary table detailing total repositories, stars, forks, contributors, commits, issues, and pull requests.

![Organization Summary Page](docs/images/dashboard_organization.png)

---

## 🛠️ Technology Stack

* **Language**: Python 3.9+
* **Cloud & Serverless**: AWS Lambda, Amazon S3
* **Data Processing**: Pandas, PyArrow, NumPy
* **Storage & Serving**: Apache Parquet, PostgreSQL, SQLAlchemy, `psycopg2-binary`
* **Frontend BI Dashboard**: Streamlit, Plotly Express
* **Configuration & Environment**: PyYAML, `python-dotenv`
* **Testing & CI/CD**: Pytest, GitHub Actions

---

## 📁 Project Structure

```
Cloud-Native-Developer-Analytics-Pipeline/
├── config/
│   └── config.yaml             # Pipeline & PostgreSQL configuration
├── dashboard/
│   ├── app.py                  # Streamlit main entry point
│   ├── database.py             # SQLAlchemy database queries & caching
│   ├── assets/
│   │   └── style.css           # GitHub-inspired clean theme CSS
│   ├── components/
│   │   ├── sidebar.py          # Logo branding, page routing & sidebar filters
│   │   ├── kpi_cards.py        # Reusable metric card renderer
│   │   └── footer.py           # Dashboard footer component
│   └── views/
│       ├── home.py             # Page 1: Executive Overview
│       ├── repository.py       # Page 2: Repository Analytics
│       ├── contributor.py      # Page 3: Contributor Analytics
│       ├── language.py         # Page 4: Language Analytics
│       ├── activity.py         # Page 5: Activity Analytics
│       └── organization.py     # Page 6: Organization Summary
├── data/                       # Local S3 Data Lake emulation
│   ├── bronze/                 # Raw ingestion layer
│   ├── silver/                 # Standardized layer
│   └── gold/                   # Aggregated metrics layer
├── docs/
│   └── images/                 # Dashboard screenshots for README
├── lambda/
│   └── lambda_function.py      # Serverless extraction handler
├── src/
│   ├── core/                   # Config loader, logger, constants
│   ├── dq/                     # Data quality rules & validators
│   ├── extract/                # GitHub API client & handlers
│   ├── pipeline/               # Bronze, Silver, Gold pipeline orchestrators
│   ├── serving/                # PostgreSQL writer & loader modules
│   └── storage/                # Parquet & S3 readers/writers
├── test/                       # Pytest unit & integration test suite
├── .env.example                # Environment variable template
├── main.py                     # CLI pipeline orchestrator
└── requirements.txt            # Unified project dependencies
```

---

## ✅ Data Quality & Metadata

The pipeline enforces data quality at every stage:
- **Null & Type Checking**: Enforces schema contracts during Silver transformations.
- **Data Quality Validation (`dq/`)**: Runs Gold layer validation checks ensuring metric consistency before database loading.
- **Metadata Logging (`MetadataWriter`)**: Writes execution metadata (row counts, file paths, status, execution timestamps) for full pipeline lineage auditing.

---

## ⚙️ How to Run

### 1. Prerequisites
- Python 3.9+
- PostgreSQL database running locally or on AWS RDS
- GitHub Personal Access Token (optional for public repos, recommended for rate limits)

### 2. Environment Setup
```bash
# Clone the repository
git clone https://github.com/dhruv-limbasiya/Cloud-Native-Developer-Analytics-Pipeline.git
cd Cloud-Native-Developer-Analytics-Pipeline

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Copy `.env.example` to `.env` and set your credentials:
```ini
GITHUB_TOKEN=your_personal_access_token
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=developer_analytics
POSTGRES_USER=postgres
```

### 4. Run the Data Pipeline
```bash
# Runs Bronze -> Silver -> Gold -> PostgreSQL loading
python main.py
```

### 5. Launch the Streamlit Dashboard
```bash
# Launch the 6-page interactive dashboard
streamlit run dashboard/app.py
```
The dashboard will open automatically at `http://localhost:8501`.

---

## 💼 Resume Summary

### Portfolio Project Bullet Points for Resume

> **Cloud-Native Developer Analytics Platform**  
> *Architected an end-to-end cloud data pipeline and BI platform ingesting GitHub API telemetry into an AWS S3 Medallion Data Lake (Bronze → Silver → Gold).*
> - **ETL & Data Lake**: Developed automated serverless extraction handlers in Python & AWS Lambda, producing partitioned Parquet datasets for Bronze, Silver, and Gold layers.
> - **Database & Serving Layer**: Modeled relational analytical schemas in PostgreSQL using SQLAlchemy to serve aggregations on repositories, languages, contributors, and activity velocity.
> - **BI Dashboard**: Built a responsive, multi-page Streamlit dashboard using Plotly and custom CSS, serving 6 executive analytics views with cached query performance (`@st.cache_data`).
> - **Quality & DevOps**: Integrated unit tests with Pytest, automated data quality validation rules, and built CI/CD workflows using GitHub Actions.