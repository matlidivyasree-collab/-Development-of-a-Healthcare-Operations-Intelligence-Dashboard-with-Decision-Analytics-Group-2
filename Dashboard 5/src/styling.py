# ================================================================
# STYLING
# Shared CSS and reusable UI components.
# One palette for the whole project so every dashboard, the sidebar,
# the text and every chart belong to the same design.
# ================================================================

import streamlit as st


# ---------------- PALETTE ----------------

NAVY = "#17324D"        # sidebar, headings, branding
TEAL = "#0F6B78"        # highlights and the most important series
BACKGROUND = "#F5F7FA"  # page background
CARD = "#FFFFFF"        # chart and card background
CHARCOAL = "#1F2937"    # primary text
SLATE = "#64748B"       # labels and supporting text
GREEN = "#16855B"       # success
AMBER = "#C98A00"       # warning
RED = "#C43D3D"         # error


# Colours for categories, ordered so the first series is teal.

CATEGORY_COLOURS = [
    TEAL,
    NAVY,
    AMBER,
    GREEN,
    SLATE,
    RED,
    "#4C8FA8",
    "#8A6D3B"
]


# Colours for a value running from low to high.

RISK_SCALE = [BACKGROUND, "#E8B84B", AMBER, RED]

VULNERABILITY_SCALE = [BACKGROUND, "#7FB8C4", TEAL, NAVY]


def apply_theme():
    """Inject the dashboard CSS. Called once from app.py.

    The colours are also set in .streamlit/config.toml. This CSS is
    kept as well so the dashboard looks the same on a machine that
    does not copy the .streamlit folder.
    """

    st.markdown(
        f"""
        <style>

        /* ---------- Page ---------- */

        .stApp {{
            background-color: {BACKGROUND};
        }}

        .stApp, .stApp p, .stApp li, .stApp label, .stApp span {{
            color: {CHARCOAL};
        }}

        .stApp h1, .stApp h2, .stApp h3, .stApp h4 {{
            color: {NAVY} !important;
        }}

        /* A teal rule under the main title. */

        .stApp h1 {{
            border-bottom: 4px solid {TEAL};
            padding-bottom: 12px;
            margin-bottom: 4px;
        }}

        /* ---------- KPI cards ---------- */

        div[data-testid="stMetric"] {{
            background-color: {CARD};
            border: 1px solid #E3E8EF;
            border-left: 5px solid {TEAL};
            border-radius: 10px;
            padding: 16px 18px;
            box-shadow: 0 1px 3px rgba(23, 50, 77, 0.08);
        }}

        /* The KPI number is held to one line and sized so that a
           short value and a long value both sit inside the same
           card. */

        div[data-testid="stMetricValue"] {{
            color: {NAVY} !important;
            font-weight: 700;
            font-size: 1.9rem !important;
            line-height: 1.2;
            white-space: nowrap;
            overflow: visible;
        }}

        div[data-testid="stMetricValue"] > div {{
            overflow: visible !important;
            text-overflow: clip !important;
        }}

        div[data-testid="stMetricLabel"] p {{
            color: {SLATE} !important;
            font-size: 0.82rem;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }}

        /* The exact figure printed under each short value. */

        div[data-testid="stMetric"] div[data-testid="stMetricDelta"] {{
            color: {SLATE} !important;
        }}

        div[data-testid="stMetric"] div[data-testid="stMetricDelta"] svg {{
            display: none;
        }}

        /* ---------- Charts sit on white cards ---------- */

        div[data-testid="stPlotlyChart"] {{
            background-color: {CARD};
            border: 1px solid #E3E8EF;
            border-radius: 10px;
            padding: 8px;
            box-shadow: 0 1px 3px rgba(23, 50, 77, 0.08);
        }}

        /* ---------- Sidebar ---------- */

        section[data-testid="stSidebar"] {{
            background-color: {NAVY};
        }}

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] p {{
            color: #E8EEF2 !important;
        }}

        /* The dropdown boxes are white with dark text so the choice
           is always readable against the navy sidebar. */

        section[data-testid="stSidebar"] div[data-baseweb="select"] > div {{
            background-color: {CARD} !important;
            border: 1px solid #3C6280 !important;
            border-radius: 6px;
        }}

        section[data-testid="stSidebar"] div[data-baseweb="select"] div,
        section[data-testid="stSidebar"] div[data-baseweb="select"] span,
        section[data-testid="stSidebar"] div[data-baseweb="select"] input {{
            color: {CHARCOAL} !important;
            -webkit-text-fill-color: {CHARCOAL} !important;
        }}

        section[data-testid="stSidebar"] div[data-baseweb="select"] svg {{
            fill: {NAVY} !important;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )


def style_chart(fig):
    """Applied to every chart so they all share one look."""

    fig.update_layout(
        paper_bgcolor=CARD,
        plot_bgcolor=CARD,
        font_color=CHARCOAL,
        title_font_color=NAVY,
        margin=dict(t=60, b=60)
    )

    fig.update_xaxes(gridcolor="#E3E8EF", zerolinecolor="#E3E8EF")
    fig.update_yaxes(gridcolor="#E3E8EF", zerolinecolor="#E3E8EF")

    return fig
