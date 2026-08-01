"""
Organization Summary Page.

Executive summary cards and high-level platform metrics table.
"""

import streamlit as st
import pandas as pd

from dashboard.components.kpi_cards import render_kpi_row
from dashboard.components.footer import render_footer


def render(org_df, repo_df, lang_df, activity_df, contributor_df, filters):
    """Render the Organization Summary page."""

    st.markdown(
        '<div class="page-title">Organization Summary</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">'
        'Executive platform summary for TensorFlow'
        '</div>',
        unsafe_allow_html=True,
    )

    if org_df.empty:
        st.info("No organization summary data available.")
        render_footer()
        return

    row = org_df.iloc[0]

    # Large Summary KPI Cards
    kpis = [
        {"label": "Repositories", "value": row.get("repositories", 0), "icon": "📦"},
        {"label": "Stars", "value": row.get("stars", 0), "icon": "⭐"},
        {"label": "Forks", "value": row.get("forks", 0), "icon": "🍴"},
        {"label": "Contributors", "value": row.get("contributors", 0), "icon": "👥"},
        {"label": "Commits", "value": row.get("commits", 0), "icon": "📝"},
        {"label": "Issues", "value": row.get("issues", 0), "icon": "🐛"},
        {"label": "Pull Requests", "value": row.get("pull_requests", 0), "icon": "🔀"},
    ]

    render_kpi_row(kpis)

    st.markdown("<br>", unsafe_allow_html=True)

    # Executive Overview Banner
    st.info(
        f"🏢 **Organization:** TensorFlow &nbsp;|&nbsp; "
        f"**Primary Language:** {row.get('primary_language', 'N/A')} &nbsp;|&nbsp; "
        f"**Total Stars:** {row.get('stars', 0):,} &nbsp;|&nbsp; "
        f"**Total Forks:** {row.get('forks', 0):,}"
    )

    # Summary Table: Metric / Value / Description
    st.markdown(
        '<div class="section-header">📊 Organization Overview Metrics</div>',
        unsafe_allow_html=True,
    )

    summary_data = [
        {"Metric": "Repositories", "Value": f"{row.get('repositories', 0):,}", "Description": "Total public repositories in TensorFlow organization"},
        {"Metric": "Stars", "Value": f"{row.get('stars', 0):,}", "Description": "Cumulative stargazers across all repositories"},
        {"Metric": "Forks", "Value": f"{row.get('forks', 0):,}", "Description": "Cumulative repository forks"},
        {"Metric": "Contributors", "Value": f"{row.get('contributors', 0):,}", "Description": "Total active code contributors"},
        {"Metric": "Commits", "Value": f"{row.get('commits', 0):,}", "Description": "Extracted commit events"},
        {"Metric": "Issues", "Value": f"{row.get('issues', 0):,}", "Description": "Tracked repository issues"},
        {"Metric": "Pull Requests", "Value": f"{row.get('pull_requests', 0):,}", "Description": "Tracked pull request submissions"},
        {"Metric": "Primary Language", "Value": str(row.get('primary_language', 'N/A')), "Description": "Top language by total code volume"},
    ]

    summary_table_df = pd.DataFrame(summary_data)

    st.dataframe(
        summary_table_df,
        width="stretch",
        hide_index=True,
    )

    render_footer()
