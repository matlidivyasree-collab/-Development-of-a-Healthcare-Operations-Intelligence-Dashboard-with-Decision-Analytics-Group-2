"""
styling.py
----------
Shared CSS and small reusable UI components (KPI tiles, section headers)
so every page of the dashboard renders with a consistent, corporate look
and feel.
"""

import streamlit as st

# --------------------------------------------------------------------------- #
# Brand palette
# --------------------------------------------------------------------------- #
PRIMARY = "#17324D"    # Deep Navy — sidebar, headings, key branding
ACCENT = "#0F6B78"     # Teal Blue — active states, buttons, highlights, key chart data
NEUTRAL_BG = "#F5F7FA"  # Off White — page background
CARD_BG = "#FFFFFF"    # White — KPI cards, tables, panels, charts
TEXT = "#1F2937"       # Charcoal — headings & primary information
MUTED = "#64748B"      # Slate — labels & supporting information
SUCCESS = "#16855B"    # Green
WARNING = "#C98A00"    # Amber
DANGER = "#C43D3D"     # Red

CUSTOM_CSS = f"""
<style>
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}

    .stApp {{
        background-color: {NEUTRAL_BG};
    }}

    .block-container {{
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }}

    /* Breathing room between stacked elements (rows, charts, tables) */
    div[data-testid="stVerticalBlock"] > div[data-testid="stHorizontalBlock"] {{
        margin-bottom: 26px;
    }}
    div[data-testid="stPlotlyChart"] {{
        margin-bottom: 6px;
    }}
    div[data-testid="stDataFrame"] {{
        margin-bottom: 6px;
    }}

    .dash-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 16px 24px;
        background: linear-gradient(90deg, {PRIMARY} 0%, {ACCENT} 100%);
        border-radius: 10px;
        color: white;
        margin-bottom: 26px;
    }}
    .dash-header h1 {{
        font-size: 1.35rem;
        margin: 0;
        font-weight: 700;
        color: white;
    }}
    .dash-header p {{
        margin: 2px 0 0 0;
        font-size: 0.82rem;
        color: #D7E4E6;
    }}
    .dash-badge {{
        background: rgba(255,255,255,0.15);
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.3px;
    }}

    .kpi-card {{
        background: {CARD_BG};
        border: 1px solid #E2E8F0;
        border-left: 4px solid {ACCENT};
        border-radius: 10px;
        padding: 16px 16px 12px 16px;
        box-shadow: 0 1px 3px rgba(23, 50, 77, 0.06);
        height: 100%;
        min-width: 0;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }}
    .kpi-label {{
        font-size: 0.68rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: {MUTED};
        font-weight: 600;
        margin-bottom: 6px;
        white-space: normal;
        overflow: visible;
        text-overflow: unset;
        word-wrap: break-word;
        line-height: 1.25;
        min-height: 2.3em;
    }}
    .kpi-value {{
        font-size: clamp(1.05rem, 1.6vw, 1.55rem);
        font-weight: 700;
        color: {TEXT};
        line-height: 1.2;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }}
    .kpi-sub {{
        font-size: 0.72rem;
        color: {MUTED};
        margin-top: 3px;
    }}

    .section-title {{
        font-size: 1.02rem;
        font-weight: 700;
        color: {TEXT};
        margin: 6px 0 4px 0;
        border-left: 4px solid {ACCENT};
        padding-left: 10px;
    }}
    .section-caption {{
        font-size: 0.78rem;
        color: {MUTED};
        padding-left: 14px;
        margin-bottom: 14px;
    }}

    /* Card-style wrapper so each chart/table reads as its own panel */
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background: {CARD_BG};
        border-radius: 10px;
    }}

    section[data-testid="stSidebar"] {{
        background-color: {PRIMARY};
    }}
    section[data-testid="stSidebar"] * {{
        color: #E8EDF1 !important;
    }}
    section[data-testid="stSidebar"] .stMarkdown h2 {{
        font-size: 1rem;
        color: #FFFFFF !important;
    }}
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {{
        background-color: rgba(255,255,255,0.08);
        border-color: rgba(255,255,255,0.25);
    }}
    section[data-testid="stSidebar"] button {{
        background-color: {ACCENT} !important;
        color: white !important;
        border: none !important;
    }}
</style>
"""


def inject_css():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def page_header(title: str, subtitle: str, badge: str = "LIVE"):
    st.markdown(
        f"""
        <div class="dash-header">
            <div>
                <h1>{title}</h1>
                <p>{subtitle}</p>
            </div>
            <div class="dash-badge">{badge}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def kpi_card(label: str, value: str, sub: str = "", color: str = PRIMARY):
    st.markdown(
        f"""
        <div class="kpi-card" style="border-left-color:{color};">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-sub">{sub}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_title(title: str, caption: str = ""):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    if caption:
        st.markdown(f'<div class="section-caption">{caption}</div>', unsafe_allow_html=True)


def coming_soon(dashboard_name: str, description: str, planned_visuals: list[str]):
    """Reserved layout for a dashboard that hasn't been built out yet.

    Keeps the page on-brand (header + card) and previews what will land
    here, so the nav item isn't just a dead end during the presentation.
    """
    st.markdown(
        f"""
        <div class="kpi-card" style="border-left-color:{ACCENT}; padding:28px 28px 24px 28px;">
            <div style="font-size:0.72rem; font-weight:700; letter-spacing:0.5px;
                        color:{ACCENT}; text-transform:uppercase; margin-bottom:8px;">
                🚧 In Development
            </div>
            <div style="font-size:1.1rem; font-weight:700; color:{TEXT}; margin-bottom:6px;">
                {dashboard_name}
            </div>
            <div style="font-size:0.88rem; color:{MUTED}; max-width:640px; line-height:1.5;">
                {description}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
    section_title("Planned Visuals", "Scoped for the next build pass")
    cols = st.columns(2, gap="large")
    for i, item in enumerate(planned_visuals):
        with cols[i % 2]:
            st.markdown(
                f"""
                <div style="background:{CARD_BG}; border:1px dashed #C7D2DA; border-radius:8px;
                            padding:14px 16px; margin-bottom:14px; font-size:0.85rem; color:{TEXT};">
                    <b>{i + 1}.</b> {item}
                </div>
                """,
                unsafe_allow_html=True,
            )