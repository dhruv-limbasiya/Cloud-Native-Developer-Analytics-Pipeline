"""
KPI Card component.

Renders a row of professional KPI cards
with large numbers, labels, SVG icons, and hover effects.
"""

import streamlit as st

# SVG Icon Dictionary for Professional Render
SVG_ICONS = {
    "Repositories": """<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#0969da" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path></svg>""",
    "Stars": """<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#e3b341" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>""",
    "Forks": """<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#1f6feb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="6" y1="3" x2="6" y2="15"></line><circle cx="18" cy="6" r="3"></circle><circle cx="6" cy="18" r="3"></circle><path d="M18 9a9 9 0 0 1-9 9"></path></svg>""",
    "Contributors": """<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#8250df" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>""",
    "Commits": """<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#1a7f37" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"></circle><line x1="1.05" y1="12" x2="8" y2="12"></line><line x1="16" y1="12" x2="22.95" y2="12"></line></svg>""",
    "Issues": """<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#cf222e" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>""",
    "Pull Requests": """<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#9a6700" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="18" r="3"></circle><circle cx="6" cy="6" r="3"></circle><path d="M13 6h3a2 2 0 0 1 2 2v7"></path><line x1="6" y1="9" x2="6" y2="21"></line></svg>""",
}


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
    Render a row of professional KPI cards with SVG icons.

    Parameters:
        kpis: list of dicts with keys:
            - label: str (e.g. "Repositories")
            - value: int/float
            - icon: str (fallback emoji or metric name)
    """

    columns = st.columns(len(kpis))

    for col, kpi in zip(columns, kpis):

        label = kpi.get("label", "")
        svg_icon = SVG_ICONS.get(label, f"""<span>{kpi.get("icon", "📊")}</span>""")

        with col:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-icon-badge">{svg_icon}</div>
                    <div class="kpi-value">{format_number(kpi["value"])}</div>
                    <div class="kpi-label">{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
