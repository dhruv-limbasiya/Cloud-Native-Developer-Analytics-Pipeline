"""
Database connection and query functions.

Reads PostgreSQL configuration from config/config.yaml
and provides cached query functions for all Gold Layer tables.
"""

import os
import yaml
import pandas as pd
import streamlit as st

from pathlib import Path
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from dotenv import load_dotenv


load_dotenv()


def get_engine():
    """
    Create SQLAlchemy engine using config/config.yaml
    and POSTGRES_PASSWORD from environment.
    """

    config_path = Path("config/config.yaml")

    if not config_path.exists():
        st.error("Configuration file not found: config/config.yaml")
        st.stop()

    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    postgres = config["postgres"]

    host = postgres["host"]
    port = postgres["port"]
    database = postgres["database"]
    username = postgres["username"]
    password = os.getenv(
        "POSTGRES_PASSWORD",
        postgres.get("password", "")
    )

    connection_string = (
        f"postgresql+psycopg2://"
        f"{username}:{quote_plus(password)}"
        f"@{host}:{port}/"
        f"{database}"
    )

    return create_engine(connection_string)


@st.cache_data(ttl=300)
def get_repository_metrics():
    """Load repository_metrics table from PostgreSQL."""

    try:
        engine = get_engine()

        df = pd.read_sql(
            "SELECT * FROM repository_metrics",
            engine
        )

        return df

    except Exception as e:
        st.error(f"Failed to load repository_metrics: {e}")
        return pd.DataFrame()


@st.cache_data(ttl=300)
def get_contributor_metrics():
    """Load contributor_metrics table from PostgreSQL."""

    try:
        engine = get_engine()

        df = pd.read_sql(
            "SELECT * FROM contributor_metrics",
            engine
        )

        return df

    except Exception as e:
        st.error(f"Failed to load contributor_metrics: {e}")
        return pd.DataFrame()


@st.cache_data(ttl=300)
def get_language_metrics():
    """Load language_metrics table from PostgreSQL."""

    try:
        engine = get_engine()

        df = pd.read_sql(
            "SELECT * FROM language_metrics",
            engine
        )

        return df

    except Exception as e:
        st.error(f"Failed to load language_metrics: {e}")
        return pd.DataFrame()


@st.cache_data(ttl=300)
def get_repository_activity():
    """Load repository_activity table from PostgreSQL."""

    try:
        engine = get_engine()

        df = pd.read_sql(
            "SELECT * FROM repository_activity",
            engine
        )

        return df

    except Exception as e:
        st.error(f"Failed to load repository_activity: {e}")
        return pd.DataFrame()


@st.cache_data(ttl=300)
def get_organization_summary():
    """Load organization_summary table from PostgreSQL."""

    try:
        engine = get_engine()

        df = pd.read_sql(
            "SELECT * FROM organization_summary",
            engine
        )

        return df

    except Exception as e:
        st.error(f"Failed to load organization_summary: {e}")
        return pd.DataFrame()
