"""
Home Page — Executive Overview.

Displays KPIs, pipeline architecture, top repositories,
language distribution, top contributors, and recent activity.
"""

import streamlit as st
import plotly.express as px
import pandas as pd

from dashboard.components.kpi_cards import render_kpi_row
from dashboard.components.footer import render_footer


# ----- Plotly Defaults -----

CHART_LAYOUT = dict(
    font_family="Inter, sans-serif",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=20, r=20, t=40, b=20),
    hoverlabel=dict(
        bgcolor="white",
        font_size=13,
        font_family="Inter, sans-serif",
    ),
)

ACCENT = "#0969da"


def render(org_df, repo_df, lang_df, activity_df, contributor_df, filters):
    """Render the Home page."""

    # ----- Title -----

    st.markdown(
        '<div class="page-title">GitHub Developer Analytics Dashboard</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">'
        'Cloud-Native Developer Analytics Platform'
        '</div>',
        unsafe_allow_html=True,
    )

    # ----- Pipeline Architecture Diagram -----

    st.markdown(
        '<div class="section-header">🏗️ Pipeline Architecture</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="pipeline-container" style="display:flex; align-items:center;
             justify-content:center; flex-wrap:wrap; gap:0.5rem;">
            <span class="pipeline-step">🐙 GitHub API</span>
            <span class="pipeline-arrow">→</span>
            <span class="pipeline-step">⚡ AWS Lambda</span>
            <span class="pipeline-arrow">→</span>
            <span class="pipeline-step">🪣 S3 Bronze</span>
            <span class="pipeline-arrow">→</span>
            <span class="pipeline-step">🥈 Silver</span>
            <span class="pipeline-arrow">→</span>
            <span class="pipeline-step">🥇 Gold</span>
            <span class="pipeline-arrow">→</span>
            <span class="pipeline-step">🐘 PostgreSQL</span>
            <span class="pipeline-arrow">→</span>
            <span class="pipeline-step">📊 Dashboard</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ----- KPI Cards -----

    if not org_df.empty:

        row = org_df.iloc[0]

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

    else:
        st.info("No organization summary data available.")

    # ----- Executive Insight Banner -----

    if not repo_df.empty and "star_count" in repo_df.columns:
        top_repo = repo_df.loc[repo_df["star_count"].idxmax()]
        st.info(
            f"💡 **Executive Summary:** TensorFlow organization manages **{len(repo_df)} repositories**. "
            f"Top repository is **{top_repo['repository_name']}** with **{top_repo['star_count']:,}** stars."
        )

    # ----- Top 10 Repositories by Stars -----

    if not repo_df.empty and "star_count" in repo_df.columns:

        st.markdown(
            '<div class="section-header">⭐ Top 10 Repositories by Stars</div>',
            unsafe_allow_html=True,
        )

        top_stars = (
            repo_df
            .nlargest(10, "star_count")
            .sort_values("star_count", ascending=True)
        )

        fig = px.bar(
            top_stars,
            x="star_count",
            y="repository_name",
            orientation="h",
            text="star_count",
            color_discrete_sequence=[ACCENT],
        )

        fig.update_traces(
            texttemplate="%{text:,.0f}",
            textposition="outside",
        )

        fig.update_layout(
            **CHART_LAYOUT,
            xaxis_title="Stars",
            yaxis_title="",
            height=400,
            showlegend=False,
        )

        st.plotly_chart(fig, width="stretch")

    # ----- Top Repositories by Forks & Language Distribution -----

    col1, col2 = st.columns(2)

    with col1:

        if not repo_df.empty and "fork_count" in repo_df.columns:

            st.markdown(
                '<div class="section-header">🍴 Top Repositories by Forks</div>',
                unsafe_allow_html=True,
            )

            top_forks = (
                repo_df
                .nlargest(10, "fork_count")
                .sort_values("fork_count", ascending=True)
            )

            fig = px.bar(
                top_forks,
                x="fork_count",
                y="repository_name",
                orientation="h",
                text="fork_count",
                color_discrete_sequence=["#1f6feb"],
            )

            fig.update_traces(
                texttemplate="%{text:,.0f}",
                textposition="outside",
            )

            fig.update_layout(
                **CHART_LAYOUT,
                xaxis_title="Forks",
                yaxis_title="",
                height=400,
                showlegend=False,
            )

            st.plotly_chart(fig, width="stretch")

    with col2:

        if not lang_df.empty and "total_bytes_of_code" in lang_df.columns:

            st.markdown(
                '<div class="section-header">💻 Language Distribution</div>',
                unsafe_allow_html=True,
            )

            lang_sorted = lang_df.sort_values(
                "total_bytes_of_code", ascending=False
            )

            top_langs = lang_sorted.head(8).copy()
            other_bytes = lang_sorted.iloc[8:]["total_bytes_of_code"].sum()

            if other_bytes > 0:
                other_row = pd.DataFrame([{
                    "language": "Other",
                    "total_bytes_of_code": other_bytes,
                }])
                top_langs = pd.concat(
                    [top_langs, other_row], ignore_index=True
                )

            fig = px.pie(
                top_langs,
                values="total_bytes_of_code",
                names="language",
                hole=0.45,
                color_discrete_sequence=px.colors.qualitative.Set2,
            )

            fig.update_traces(
                textposition="inside",
                textinfo="percent+label",
                hovertemplate="%{label}: %{value:,.0f} bytes<br>%{percent}",
            )

            fig.update_layout(
                **CHART_LAYOUT,
                height=400,
                showlegend=True,
                legend=dict(orientation="v", x=1.05, y=0.5),
            )

            st.plotly_chart(fig, width="stretch")

    # ----- Top Contributors -----

    if not contributor_df.empty and "total_contributions" in contributor_df.columns:

        st.markdown(
            '<div class="section-header">👥 Top Contributors by Repository</div>',
            unsafe_allow_html=True,
        )

        top_contributors = (
            contributor_df
            .nlargest(10, "total_contributions")
            .sort_values("total_contributions", ascending=True)
        )

        fig = px.bar(
            top_contributors,
            x="total_contributions",
            y="repository_name",
            orientation="h",
            text="total_contributions",
            color_discrete_sequence=["#1a7f37"],
        )

        fig.update_traces(
            texttemplate="%{text:,.0f}",
            textposition="outside",
        )

        fig.update_layout(
            **CHART_LAYOUT,
            xaxis_title="Total Contributions",
            yaxis_title="",
            height=350,
            showlegend=False,
        )

        st.plotly_chart(fig, width="stretch")

    # ----- Factual Recent Activity Table -----

    if not activity_df.empty:

        st.markdown(
            '<div class="section-header">📋 Recent Repository Activity</div>',
            unsafe_allow_html=True,
        )

        display_df = activity_df.rename(columns={
            "repository_name": "Repository",
            "commit_count": "Commits",
            "issue_count": "Open Issues",
            "pull_request_count": "Pull Requests",
            "total_activity": "Total Activity",
        })

        st.dataframe(
            display_df[[
                "Repository", "Commits", "Open Issues",
                "Pull Requests", "Total Activity"
            ]],
            width="stretch",
            hide_index=True,
        )

    # ----- Footer -----

    render_footer()
