"""
Repository Analytics Page.

Displays repository metrics: stars, forks, watchers,
size analysis, and a searchable repository table.
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

ACCENT = "#0969da"


def render(repo_df, filters):
    """Render the Repository Analytics page."""

    st.markdown(
        '<div class="page-title">Repository Analytics</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">'
        'Detailed analysis of repository metrics across the organization'
        '</div>',
        unsafe_allow_html=True,
    )

    if repo_df.empty:
        st.info("No repository data available.")
        render_footer()
        return

    # Apply filters
    filtered_df = repo_df.copy()

    if filters.get("language") and filters["language"] != "All Languages":
        filtered_df = filtered_df[
            filtered_df["language"] == filters["language"]
        ]

    if filters.get("search"):
        search = filters["search"].lower()
        filtered_df = filtered_df[
            filtered_df["repository_name"].str.lower().str.contains(
                search, na=False
            )
        ]

    if filtered_df.empty:
        st.warning("No repositories match the current filters.")
        render_footer()
        return

    # ----- Top Repositories by Stars -----

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            '<div class="section-header">⭐ Top Repositories by Stars</div>',
            unsafe_allow_html=True,
        )

        top_stars = (
            filtered_df
            .nlargest(15, "star_count")
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
            height=500,
            showlegend=False,
        )

        st.plotly_chart(fig, width="stretch")

    with col2:

        st.markdown(
            '<div class="section-header">🍴 Top Repositories by Forks</div>',
            unsafe_allow_html=True,
        )

        top_forks = (
            filtered_df
            .nlargest(15, "fork_count")
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
            height=500,
            showlegend=False,
        )

        st.plotly_chart(fig, width="stretch")

    # ----- Watchers vs Stars (Scatter Plot) -----

    st.markdown(
        '<div class="section-header">👁️ Watchers vs Stars</div>',
        unsafe_allow_html=True,
    )

    fig = px.scatter(
        filtered_df,
        x="star_count",
        y="watcher_count",
        size="fork_count",
        color="language",
        hover_name="repository_name",
        hover_data=["fork_count", "open_issue_count"],
        color_discrete_sequence=px.colors.qualitative.Set2,
        size_max=40,
    )

    fig.update_layout(
        **CHART_LAYOUT,
        xaxis_title="Stars",
        yaxis_title="Watchers",
        height=450,
        legend_title="Language",
    )

    st.plotly_chart(fig, width="stretch")

    # ----- Repository Size -----

    st.markdown(
        '<div class="section-header">📏 Repository Size (KB)</div>',
        unsafe_allow_html=True,
    )

    top_size = (
        filtered_df
        .nlargest(15, "size")
        .sort_values("size", ascending=True)
    )

    fig = px.bar(
        top_size,
        x="size",
        y="repository_name",
        orientation="h",
        text="size",
        color_discrete_sequence=["#8250df"],
    )

    fig.update_traces(
        texttemplate="%{text:,.0f}",
        textposition="outside",
    )

    fig.update_layout(
        **CHART_LAYOUT,
        xaxis_title="Size (KB)",
        yaxis_title="",
        height=500,
        showlegend=False,
    )

    st.plotly_chart(fig, width="stretch")

    # ----- Repository Statistics Table -----

    st.markdown(
        '<div class="section-header">📋 Repository Statistics</div>',
        unsafe_allow_html=True,
    )

    display_df = filtered_df.copy()

    if "created_at" in display_df.columns and hasattr(display_df["created_at"], "dt"):
        display_df["created_at"] = display_df["created_at"].dt.strftime(
            "%Y-%m-%d"
        )

    display_df = display_df.rename(columns={
        "repository_name": "Repository",
        "star_count": "Stars",
        "fork_count": "Forks",
        "watcher_count": "Watchers",
        "open_issue_count": "Open Issues",
        "language": "Language",
        "size": "Size (KB)",
        "created_at": "Created",
    })

    table_cols = [
        "Repository", "Stars", "Forks", "Watchers",
        "Open Issues", "Language", "Size (KB)", "Created",
    ]

    available_cols = [c for c in table_cols if c in display_df.columns]

    st.dataframe(
        display_df[available_cols].sort_values("Stars", ascending=False),
        width="stretch",
        hide_index=True,
        height=500,
    )

    # ----- Footer -----

    render_footer()
