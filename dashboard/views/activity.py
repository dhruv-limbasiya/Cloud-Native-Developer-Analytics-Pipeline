"""
Activity Analytics Page.

Displays repository activity breakdown:
Commits, Issues, and Pull Requests.
"""

import streamlit as st
import plotly.express as px

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


def render(activity_df, filters):
    """Render the Activity Analytics page."""

    st.markdown(
        '<div class="page-title">Activity Analytics</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">'
        'Commit, issue, and pull request activity across repositories'
        '</div>',
        unsafe_allow_html=True,
    )

    if activity_df.empty:
        st.info("No repository activity data available.")
        render_footer()
        return

    # Apply repo filter if set
    filtered_df = activity_df.copy()

    if filters.get("repository") and filters["repository"] != "All Repositories":
        filtered_df = filtered_df[
            filtered_df["repository_name"] == filters["repository"]
        ]

    if filtered_df.empty:
        st.warning("No activity metrics match the current repository filter.")
        render_footer()
        return

    total_commits = filtered_df["commit_count"].sum()
    total_issues = filtered_df["issue_count"].sum()
    total_prs = filtered_df["pull_request_count"].sum()

    st.info(
        f"💡 **Activity Overview:** Total activity includes **{total_commits:,}** commits, "
        f"**{total_issues:,}** open issues, and **{total_prs:,}** pull requests."
    )

    # 3 Column Bar Charts for Commits, Issues, PRs
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            '<div class="section-header">📝 Commits by Repo</div>',
            unsafe_allow_html=True,
        )
        top_commits = filtered_df.nlargest(10, "commit_count").sort_values("commit_count", ascending=True)

        fig = px.bar(
            top_commits,
            x="commit_count",
            y="repository_name",
            orientation="h",
            text="commit_count",
            color_discrete_sequence=["#0969da"],
        )
        fig.update_layout(**CHART_LAYOUT, xaxis_title="Commits", yaxis_title="", height=350, showlegend=False)
        st.plotly_chart(fig, width="stretch")

    with col2:
        st.markdown(
            '<div class="section-header">🐛 Issues by Repo</div>',
            unsafe_allow_html=True,
        )
        top_issues = filtered_df.nlargest(10, "issue_count").sort_values("issue_count", ascending=True)

        fig = px.bar(
            top_issues,
            x="issue_count",
            y="repository_name",
            orientation="h",
            text="issue_count",
            color_discrete_sequence=["#cf222e"],
        )
        fig.update_layout(**CHART_LAYOUT, xaxis_title="Issues", yaxis_title="", height=350, showlegend=False)
        st.plotly_chart(fig, width="stretch")

    with col3:
        st.markdown(
            '<div class="section-header">🔀 Pull Requests by Repo</div>',
            unsafe_allow_html=True,
        )
        top_prs = filtered_df.nlargest(10, "pull_request_count").sort_values("pull_request_count", ascending=True)

        fig = px.bar(
            top_prs,
            x="pull_request_count",
            y="repository_name",
            orientation="h",
            text="pull_request_count",
            color_discrete_sequence=["#1a7f37"],
        )
        fig.update_layout(**CHART_LAYOUT, xaxis_title="Pull Requests", yaxis_title="", height=350, showlegend=False)
        st.plotly_chart(fig, width="stretch")

    # ----- Activity Table -----

    st.markdown(
        '<div class="section-header">📋 Repository Activity Table</div>',
        unsafe_allow_html=True,
    )

    display_df = filtered_df.rename(columns={
        "repository_name": "Repository",
        "commit_count": "Commits",
        "issue_count": "Issues",
        "pull_request_count": "Pull Requests",
        "total_activity": "Total Activity",
    })

    st.dataframe(
        display_df[["Repository", "Commits", "Issues", "Pull Requests", "Total Activity"]].sort_values("Total Activity", ascending=False),
        width="stretch",
        hide_index=True,
    )

    render_footer()
