# Streamlit Community Cloud Deployment Guide

This guide details how to deploy the **GitHub Developer Analytics Dashboard** for free on **Streamlit Community Cloud** so recruiters can access your live interactive dashboard.

---

## 📋 Prerequisites

1. Your repository pushed to GitHub:  
   `https://github.com/dhruv-limbasiya/Cloud-Native-Developer-Analytics-Pipeline`
2. A free account on [share.streamlit.io](https://share.streamlit.io/) linked to your GitHub account.
3. A publicly accessible PostgreSQL database (e.g., free tier instance on **ElephantSQL**, **Neon.tech**, **Supabase**, or **AWS RDS**).

---

## 🚀 Deployment Steps

### Step 1: Sign in to Streamlit Community Cloud
- Go to [share.streamlit.io](https://share.streamlit.io/)
- Click **"Sign in with GitHub"**

### Step 2: Create a New App
- Click **"Create app"**
- Select **"I already have an app"**
- Set the deployment parameters:
  - **Repository**: `dhruv-limbasiya/Cloud-Native-Developer-Analytics-Pipeline`
  - **Branch**: `master`
  - **Main file path**: `dashboard/app.py`

### Step 3: Configure Environment Secrets
Click **"Advanced settings..."** → **"Secrets"** and enter your production PostgreSQL credentials:

```toml
[postgres]
host = "your-database-host.neon.tech"
port = 5432
database = "developer_analytics"
username = "postgres"
password = "your-secure-password"

POSTGRES_PASSWORD = "your-secure-password"
```

### Step 4: Deploy!
- Click **"Deploy!"**
- Streamlit will automatically install dependencies from `requirements.txt` and launch your 6-page dashboard.
- You will receive a permanent live URL (e.g. `https://developer-analytics.streamlit.app`) to share on your resume and LinkedIn!
