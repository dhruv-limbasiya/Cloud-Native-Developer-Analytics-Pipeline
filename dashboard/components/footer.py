"""
Footer component.

Renders a consistent footer at the bottom of every page.
"""

import streamlit as st


def render_footer():
    """Render the dashboard footer with tech stack."""

    st.markdown(
        """
        <div class="footer">
            <strong>Cloud-Native Developer Analytics Platform</strong><br>
            Built with &nbsp;
            🐍 Python &nbsp;·&nbsp;
            📊 Streamlit &nbsp;·&nbsp;
            ☁️ AWS &nbsp;·&nbsp;
            🐘 PostgreSQL &nbsp;·&nbsp;
            📈 Plotly &nbsp;·&nbsp;
            🐙 GitHub API
        </div>
        """,
        unsafe_allow_html=True,
    )
