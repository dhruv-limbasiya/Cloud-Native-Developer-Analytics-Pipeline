"""
KPI Card component.

Renders a row of professional KPI cards
with large numbers, labels, icons, and hover effects.
"""

import streamlit as st


def format_number(value):
    """Format large numbers with K/M suffixes."""

    if value is None:
        return "0"

    value = int(value)

    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"

    if value >= 1_000:
        return f"{value / 1_000:.1f}K"

    return f"{value:,}"


def render_kpi_row(kpis):
    """
    Render a row of KPI cards.

    Parameters:
        kpis: list of dicts with keys:
            - label: str (e.g. "Repositories")
            - value: int/float
            - icon: str (emoji)
    """

    columns = st.columns(len(kpis))

    for col, kpi in zip(columns, kpis):

        with col:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-icon">{kpi["icon"]}</div>
                    <div class="kpi-value">{format_number(kpi["value"])}</div>
                    <div class="kpi-label">{kpi["label"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
