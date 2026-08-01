"""
Contributor Analytics Page.

Displays top contributors, contribution distribution,
per-repository breakdown, and contributor leaderboard.
"""

import streamlit as st
import plotly.express as px

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


def render(contributor_df, repo_df, filters):
    """Render the Contributor Analytics page."""

    st.markdown(
        '<div class="page-title">Contributor Analytics</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">'
        'Analysis of contributor activity and engagement'
        '</div>',
        unsafe_allow_html=True,
    )

    if contributor_df.empty:
        st.info("No contributor data available.")
        render_footer()
        return

    # ----- KPI Summary -----

    total_contributors = contributor_df["contributor_count"].sum()
    total_contributions = contributor_df["total_contributions"].sum()
    avg_contributions = contributor_df["average_contributions"].mean()

    kpis = [
        {"label": "Total Contributors", "value": total_contributors, "icon": "👥"},
        {"label": "Total Contributions", "value": total_contributions, "icon": "📝"},
        {"label": "Avg Contributions / Repo", "value": int(avg_contributions), "icon": "📊"},
        {"label": "Repositories", "value": len(contributor_df), "icon": "📦"},
    ]

    render_kpi_row(kpis)

    st.markdown("<br>", unsafe_allow_html=True)

    # ----- Top Contributors by Total Contributions -----

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            '<div class="section-header">🏆 Top Contributing Repositories</div>',
            unsafe_allow_html=True,
        )

        top_repos = (
            contributor_df
            .nlargest(10, "total_contributions")
            .sort_values("total_contributions", ascending=True)
        )

        fig = px.bar(
            top_repos,
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
            height=400,
            showlegend=False,
        )

        st.plotly_chart(fig, width="stretch")

    with col2:

        st.markdown(
            '<div class="section-header">👥 Contributor Count by Repository</div>',
            unsafe_allow_html=True,
        )

        top_count = (
            contributor_df
            .nlargest(10, "contributor_count")
            .sort_values("contributor_count", ascending=True)
        )

        fig = px.bar(
            top_count,
            x="contributor_count",
            y="repository_name",
            orientation="h",
            text="contributor_count",
            color_discrete_sequence=["#0969da"],
        )

        fig.update_traces(
            texttemplate="%{text:,.0f}",
            textposition="outside",
        )

        fig.update_layout(
            **CHART_LAYOUT,
            xaxis_title="Contributors",
            yaxis_title="",
            height=400,
            showlegend=False,
        )

        st.plotly_chart(fig, width="stretch")

    # ----- Contributions Distribution (Histogram) -----

    st.markdown(
        '<div class="section-header">📊 Contributions Distribution</div>',
        unsafe_allow_html=True,
    )

    fig = px.histogram(
        contributor_df,
        x="total_contributions",
        nbins=20,
        color_discrete_sequence=["#8250df"],
        labels={"total_contributions": "Total Contributions"},
    )

    fig.update_layout(
        **CHART_LAYOUT,
        xaxis_title="Total Contributions",
        yaxis_title="Number of Repositories",
        height=350,
        showlegend=False,
    )

    st.plotly_chart(fig, width="stretch")

    # ----- Contributor Leaderboard -----

    st.markdown(
        '<div class="section-header">🏅 Repository Contributor Leaderboard</div>',
        unsafe_allow_html=True,
    )

    leaderboard = contributor_df.copy()
    leaderboard = leaderboard.sort_values(
        "total_contributions", ascending=False
    )

    leaderboard["rank"] = range(1, len(leaderboard) + 1)

    display_df = leaderboard.rename(columns={
        "rank": "Rank",
        "repository_name": "Repository",
        "contributor_count": "Contributors",
        "total_contributions": "Total Contributions",
        "average_contributions": "Avg Contributions",
    })

    st.dataframe(
        display_df[[
            "Rank", "Repository", "Contributors",
            "Total Contributions", "Avg Contributions"
        ]],
        width="stretch",
        hide_index=True,
    )

    # ----- Average Contributions Comparison -----

    st.markdown(
        '<div class="section-header">📈 Average Contributions per Contributor</div>',
        unsafe_allow_html=True,
    )

    sorted_df = contributor_df.sort_values(
        "average_contributions", ascending=True
    )

    fig = px.bar(
        sorted_df,
        x="average_contributions",
        y="repository_name",
        orientation="h",
        text="average_contributions",
        color_discrete_sequence=["#cf222e"],
    )

    fig.update_traces(
        texttemplate="%{text:.1f}",
        textposition="outside",
    )

    fig.update_layout(
        **CHART_LAYOUT,
        xaxis_title="Average Contributions per Contributor",
        yaxis_title="",
        height=350,
        showlegend=False,
    )

    st.plotly_chart(fig, width="stretch")

    # ----- Footer -----

    render_footer()
