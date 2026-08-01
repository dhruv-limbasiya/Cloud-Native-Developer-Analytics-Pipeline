"""
Sidebar component.

Renders the dashboard sidebar with logo, navigation,
and global filters.
"""

import streamlit as st


def render_sidebar(repo_df, lang_df):
    """
    Render sidebar with logo, navigation, and filters.

    Parameters:
        repo_df: Repository metrics DataFrame (for filter options)
        lang_df: Language metrics DataFrame (for filter options)

    Returns:
        dict with selected_page, selected_repo, selected_language, search
    """

    with st.sidebar:

        # ----- Logo -----

        st.markdown(
            """
            <div class="sidebar-logo">
                <div class="logo-icon-badge">
                    <svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>
                    </svg>
                </div>
                <div class="logo-title">Cloud-Native<br>Developer Analytics</div>
                <div class="logo-subtitle">Enterprise Telemetry Platform</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ----- Navigation -----

        st.markdown("#### Navigation")

        selected_page = st.radio(
            "Go to",
            [
                "⚡ Home Overview",
                "📦 Repository Analytics",
                "👥 Contributor Analytics",
                "💻 Language Analytics",
                "📊 Activity Analytics",
                "🏢 Organization Summary",
            ],
            label_visibility="collapsed",
        )

        st.markdown("---")

        # ----- Filters -----

        st.markdown("#### Filters")

        # Fixed Organization Display
        st.markdown(
            """
            <div style="margin-bottom: 1rem; background: #f6f8fa; padding: 0.6rem 0.8rem; border-radius: 6px; border: 1px solid #d0d7de;">
                <div style="font-size: 0.75rem; font-weight: 600; color: #57606a; text-transform: uppercase; letter-spacing: 0.5px;">ORGANIZATION</div>
                <div style="font-weight: 700; font-size: 0.95rem; color: #0969da; display: flex; align-items: center; gap: 0.4rem;">
                    <span>🏢</span> TensorFlow
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Repository filter
        repo_options = ["All Repositories"]

        if not repo_df.empty and "repository_name" in repo_df.columns:
            repo_options += sorted(repo_df["repository_name"].unique().tolist())

        selected_repo = st.selectbox(
            "Repository",
            repo_options,
            index=0,
        )

        # Language filter
        lang_options = ["All Languages"]

        if not lang_df.empty and "language" in lang_df.columns:
            lang_options += sorted(lang_df["language"].unique().tolist())

        selected_language = st.selectbox(
            "Language",
            lang_options,
            index=0,
        )

        # Search
        search_query = st.text_input(
            "🔍 Search Repository",
            placeholder="Type repository name...",
        )

    return {
        "page": selected_page,
        "organization": "tensorflow",
        "repository": selected_repo,
        "language": selected_language,
        "search": search_query,
    }
