"""
GitHub Developer Analytics Dashboard.

Main Streamlit application entry point.
Run from project root:
    streamlit run dashboard/app.py
"""

import streamlit as st

from pathlib import Path

from dashboard.database import (
    get_repository_metrics,
    get_contributor_metrics,
    get_language_metrics,
    get_repository_activity,
    get_organization_summary,
)

from dashboard.components.sidebar import render_sidebar

from dashboard.views import (
    home,
    repository,
    contributor,
    language,
    activity,
    organization,
)


# ----- Page Config -----

st.set_page_config(
    page_title="GitHub Developer Analytics",
    page_icon="🐙",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ----- Load Custom CSS -----

css_path = Path(__file__).parent / "assets" / "style.css"

if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# ----- Load Data -----

with st.spinner("Loading data from PostgreSQL..."):

    repo_df = get_repository_metrics()
    contributor_df = get_contributor_metrics()
    lang_df = get_language_metrics()
    activity_df = get_repository_activity()
    org_df = get_organization_summary()


# ----- Sidebar -----

filters = render_sidebar(repo_df, lang_df)


# ----- Page Routing -----

page = filters["page"]

if page == "🏠 Home":
    home.render(org_df, repo_df, lang_df, activity_df, contributor_df, filters)

elif page == "📦 Repository Analytics":
    repository.render(repo_df, filters)

elif page == "👥 Contributor Analytics":
    contributor.render(contributor_df, repo_df, filters)

elif page == "💻 Language Analytics":
    language.render(lang_df, filters)

elif page == "📊 Activity Analytics":
    activity.render(activity_df, filters)

elif page == "🏢 Organization Summary":
    organization.render(org_df, repo_df, lang_df, activity_df, contributor_df, filters)
