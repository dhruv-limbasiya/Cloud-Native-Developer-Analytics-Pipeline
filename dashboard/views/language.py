"""
Language Analytics Page.

Displays language breakdown across repositories,
byte counts, donut distribution, and top languages table.
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


def render(lang_df, filters):
    """Render the Language Analytics page."""

    st.markdown(
        '<div class="page-title">Language Analytics</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">'
        'Programming language usage and volume across the organization'
        '</div>',
        unsafe_allow_html=True,
    )

    if lang_df.empty:
        st.info("No language data available.")
        render_footer()
        return

    # Apply search/language filters if applicable
    filtered_df = lang_df.copy()

    if filters.get("language") and filters["language"] != "All Languages":
        filtered_df = filtered_df[
            filtered_df["language"] == filters["language"]
        ]

    if filtered_df.empty:
        st.warning("No language metrics match the selected filter.")
        render_footer()
        return

    # Summary insight
    top_lang = filtered_df.loc[filtered_df["total_bytes_of_code"].idxmax()]
    st.info(
        f"💡 **Language Insight:** Primary language is **{top_lang['language']}** with "
        f"**{top_lang['total_bytes_of_code']:,}** total bytes of code across **{top_lang['repository_count']}** repositories."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            '<div class="section-header">🍩 Programming Language Distribution</div>',
            unsafe_allow_html=True,
        )

        fig = px.pie(
            filtered_df.head(10),
            values="total_bytes_of_code",
            names="language",
            hole=0.45,
            color_discrete_sequence=px.colors.qualitative.Bold,
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
        )

        st.plotly_chart(fig, width="stretch")

    with col2:
        st.markdown(
            '<div class="section-header">📊 Top Languages by Code Volume</div>',
            unsafe_allow_html=True,
        )

        top_vol = filtered_df.head(10).sort_values("total_bytes_of_code", ascending=True)

        fig = px.bar(
            top_vol,
            x="total_bytes_of_code",
            y="language",
            orientation="h",
            text="total_bytes_of_code",
            color_discrete_sequence=["#0969da"],
        )

        fig.update_traces(
            texttemplate="%{text:,.0f} bytes",
            textposition="outside",
        )

        fig.update_layout(
            **CHART_LAYOUT,
            xaxis_title="Bytes of Code",
            yaxis_title="",
            height=400,
            showlegend=False,
        )

        st.plotly_chart(fig, width="stretch")

    # ----- Language Statistics Table -----

    st.markdown(
        '<div class="section-header">📋 Language Statistics</div>',
        unsafe_allow_html=True,
    )

    display_df = filtered_df.copy()

    total_bytes = display_df["total_bytes_of_code"].sum()
    if total_bytes > 0:
        display_df["Percentage"] = (
            (display_df["total_bytes_of_code"] / total_bytes) * 100
        ).round(2).astype(str) + " %"
    else:
        display_df["Percentage"] = "0 %"

    display_df = display_df.rename(columns={
        "language": "Language",
        "repository_count": "Repositories",
        "total_bytes_of_code": "Total Bytes",
        "average_bytes_per_repository": "Avg Bytes / Repo",
    })

    table_cols = ["Language", "Repositories", "Total Bytes", "Avg Bytes / Repo", "Percentage"]
    available_cols = [c for c in table_cols if c in display_df.columns]

    st.dataframe(
        display_df[available_cols].sort_values("Repositories", ascending=False),
        width="stretch",
        hide_index=True,
    )

    render_footer()
