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

    /* ================================
       NATIVE st.metric() KPI CARDS
       (used on pages that need delta/MoM indicators, e.g. Executive
       Overview, Laboratory & Healthcare Capacity)
       ================================ */
    div[data-testid="stMetric"] {{
        background-color: {CARD_BG} !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 12px !important;
        padding: 14px 16px !important;
        box-shadow: 0 1px 3px rgba(23, 50, 77, 0.06) !important;
        min-height: 105px !important;
        box-sizing: border-box !important;
    }}
    div[data-testid="stMetricLabel"],
    div[data-testid="stMetricLabel"] *,
    [data-testid="stMetricLabel"] p,
    [data-testid="stMetricLabel"] div,
    [data-testid="stMetricLabel"] span {{
        color: {TEXT} !important;
        opacity: 1 !important;
        visibility: visible !important;
        -webkit-text-fill-color: {TEXT} !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        white-space: normal !important;
        word-break: break-word !important;
        line-height: 1.2 !important;
    }}
    div[data-testid="stMetricValue"],
    div[data-testid="stMetricValue"] *,
    [data-testid="stMetricValue"] div,
    [data-testid="stMetricValue"] span {{
        color: {PRIMARY} !important;
        opacity: 1 !important;
        visibility: visible !important;
        -webkit-text-fill-color: {PRIMARY} !important;
        font-size: 25px !important;
        font-weight: 700 !important;
    }}
    div[data-testid="stMetric"] p {{
        opacity: 1 !important;
        color: {TEXT} !important;
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


def kpi_card(label: str, value: str, sub: str = "", color: str = PRIMARY, bg: str = None):
    bg_style = f"background:{bg};" if bg else ""
    st.markdown(
        f"""
        <div class="kpi-card" style="border-left-color:{color};{bg_style}">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-sub">{sub}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def kpi_card_delta(label: str, value: str, delta: str = None, color: str = PRIMARY,
                    bg: str = None, invert: bool = False, badge: str = None, badge_color: str = None):
    """Like kpi_card(), but renders a small colored MoM delta line underneath
    the value (e.g. "▲ +3.6% MoM" in green, "▼ -4.1% MoM" in red) — used on
    pages migrated from native st.metric() that need per-card background
    colors, which st.metric() can't do.

    invert=True flips which direction counts as "good" (e.g. a rising
    positivity rate is bad, so its delta should read red even though it's
    an increase).
    """
    delta_html = ""
    if delta:
        is_up = delta.strip().startswith("+")
        good = is_up if not invert else not is_up
        delta_color = SUCCESS if good else DANGER
        arrow = "▲" if is_up else "▼"
        delta_html = (
            f'<div style="font-size:0.72rem; font-weight:700; color:{delta_color}; margin-top:4px;">'
            f"{arrow} {delta.lstrip('+-')}</div>"
        )

    badge_html = ""
    if badge:
        bc = badge_color or color
        badge_html = (
            f'<span style="background:{bc}22; color:{bc}; padding:2px 8px; border-radius:6px; '
            f'font-size:0.66rem; font-weight:700; border:1px solid {bc}55; margin-left:auto;">{badge}</span>'
        )

    bg_style = f"background:{bg};" if bg else ""
    # Built as one unbroken line (no internal newlines) rather than an
    # indented multi-line f-string: when badge_html/delta_html are empty,
    # a multi-line version leaves a blank/whitespace-only line, which
    # terminates Streamlit's markdown HTML-block parsing early and causes
    # everything after it to render as a literal code block instead of HTML.
    html = (
        f'<div class="kpi-card" style="border-left-color:{color};{bg_style}">'
        f'<div style="display:flex; justify-content:space-between; align-items:center;">'
        f'<div class="kpi-label" style="margin-bottom:0;">{label}</div>'
        f'{badge_html}'
        f'</div>'
        f'<div class="kpi-value">{value}</div>'
        f'{delta_html}'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


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


GEOGRAPHIC_CSS = """<style>
:root {
    --bg: #F5F7FA;
    --panel: #FFFFFF;
    --panel2: #17324D;
    --line: #D9E1E8;
    --text: #1F2937;
    --muted: #64748B;
    --teal: #0F6B78;
    --blue: #0F6B78;
    --amber: #C98A00;
    --orange: #C98A00;
    --red: #C43D3D;
}

html, body, [class*="css"] {
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
                 "Segoe UI", sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 15% -5%, rgba(72,224,192,.10), transparent 24%),
        radial-gradient(circle at 95% 5%, rgba(105,169,255,.08), transparent 22%),
        var(--bg);
    color: var(--text);
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #122B45 0%, #173A59 100%) !important;
    border-right: none !important;
}

[data-testid="stSidebar"] > div:first-child {
    padding: 0 16px 18px !important;
}

[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

[data-testid="stSidebar"] .stMarkdown {
    margin-bottom: 0 !important;
}

[data-testid="stSidebar"] h2 {
    font-size: 1.05rem !important;
    font-weight: 800 !important;
    letter-spacing: -.02em !important;
    margin: 6px 0 2px !important;
}

[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
    color: rgba(255,255,255,.72) !important;
    font-size: .74rem !important;
    line-height: 1.55 !important;
}

[data-testid="stSidebar"] hr {
    margin: 18px 0 20px !important;
    border-color: rgba(255,255,255,.12) !important;
}

[data-testid="stSidebar"] label {
    color: #F7FBFF !important;
    font-size: .72rem !important;
    font-weight: 650 !important;
    letter-spacing: .01em !important;
}

[data-testid="stSidebar"] .stSelectbox {
    margin-bottom: 13px !important;
}

[data-testid="stSidebar"] .stSelectbox > div > div {
    border-radius: 10px !important;
}

/* Keep sidebar labels white, but make selected filter values readable. */
[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background: rgba(255,255,255,.08) !important;
    border: 1px solid rgba(255,255,255,.16) !important;
    border-radius: 10px !important;
    min-height: 42px !important;
    box-shadow: none !important;
}
/* Force the CURRENT selected value to be visible inside every sidebar selectbox.
   Streamlit/BaseWeb can render the value as a nested div rather than a
   data-baseweb="select-value" element, so target the complete value tree. */
[data-testid="stSidebar"] div[data-baseweb="select"] [role="button"],
[data-testid="stSidebar"] div[data-baseweb="select"] [role="button"] > div,
[data-testid="stSidebar"] div[data-baseweb="select"] [role="button"] div,
[data-testid="stSidebar"] div[data-baseweb="select"] [role="button"] span,
[data-testid="stSidebar"] div[data-baseweb="select"] input,
[data-testid="stSidebar"] div[data-baseweb="select"] [class*="singleValue"],
[data-testid="stSidebar"] div[data-baseweb="select"] [class*="placeholder"] {
    color: #F8FBFF !important;
    -webkit-text-fill-color: #F8FBFF !important;
    opacity: 1 !important;
}
[data-testid="stSidebar"] div[data-baseweb="select"] [aria-selected="true"] {
    color: #1F2937 !important;
    background: #FFFFFF !important;
}
/* Do not let the sidebar-wide white-text rule hide selectbox values. */
[data-testid="stSidebar"] div[data-baseweb="select"] * {
    -webkit-text-fill-color: #F8FBFF !important;
}
[data-testid="stSidebar"] div[data-baseweb="select"] svg {
    fill: #64748B !important;
    color: #64748B !important;
    -webkit-text-fill-color: #64748B !important;
}
[data-testid="stSidebar"] div[data-baseweb="select"] svg {
    fill: #64748B !important;
}
/* Dropdown menu */
div[data-baseweb="popover"] li {
    color: #1F2937 !important;
    background: #FFFFFF !important;
}
div[data-baseweb="popover"] li:hover {
    background: #F5F7FA !important;
}

[data-testid="stAppViewContainer"] > .main {
    width: 100% !important;
}

[data-testid="stAppViewContainer"] > .main > div {
    width: 100% !important;
}

[data-testid="stAppViewContainer"] .block-container {
    width: 100% !important;
    max-width: none !important;
    margin-left: 0 !important;
    margin-right: 0 !important;
    padding-top: 1.45rem;
    padding-bottom: 1.5rem;
}

 .hero {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 18px;
    margin: 0 0 18px 0;
    padding: 22px 30px;
    min-height: 120px;
    box-sizing: border-box;
    border-radius: 13px;
    background: linear-gradient(105deg, #223752 0%, #286879 100%);
    box-shadow: 0 7px 20px rgba(20,48,72,.13);
}

.hero-left {
    min-width: 0;
}

.eyebrow {
    display: none;
}

.hero-title {
    margin: 0;
    color: #ffffff;
    font-size: 1.5rem;
    line-height: 1.15;
    letter-spacing: -.01em;
    font-weight: 800;
}

.hero-subtitle {
    color: rgba(255,255,255,.82);
    margin-top: 10px;
    font-size: .88rem;
    line-height: 1.35;
    max-width: 850px;
}

.hero-badge {
    flex: 0 0 auto;
    border: 0;
    background: rgba(255,255,255,.16);
    color: #ffffff;
    padding: 7px 11px;
    border-radius: 999px;
    font-size: .62rem;
    font-weight: 800;
    letter-spacing: .03em;
}

.kpi-grid {
    display: grid;
    grid-template-columns: repeat(8, minmax(0, 1fr));
    gap: 10px;
    margin: 0 0 22px;
}

.kpi {
    height: 136px !important;
    padding: 18px 18px 15px !important;
    border-radius: 15px !important;
    border: 1px solid #DCE3EA !important;
    border-left: 4px solid #17324D !important;
    background: #FFFFFF;
    box-shadow: 0 7px 20px rgba(23,50,77,.07) !important;
}

.kpi:nth-child(2) { border-left-color: #17324D !important; }
.kpi:nth-child(3) { border-left-color: #D89B00 !important; }
.kpi:nth-child(4) { border-left-color: #2B8B70 !important; }
.kpi:nth-child(5) { border-left-color: #C84343 !important; }
.kpi:nth-child(6) { border-left-color: #2B8B70 !important; }
.kpi:nth-child(7) { border-left-color: #2B8B70 !important; }
.kpi:nth-child(8) { border-left-color: #C84343 !important; }

.kpi-label {
    color: #6E8194 !important;
    font-size: .65rem !important;
    line-height: 1.2 !important;
    font-weight: 800 !important;
    text-transform: uppercase;
    letter-spacing: .075em;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.kpi-value {
    color: #172A40 !important;
    font-size: 1.55rem !important;
    line-height: 1 !important;
    font-weight: 850 !important;
    white-space: nowrap;
}

.kpi-meta {
    color: #176A77 !important;
    font-size: .66rem !important;
    font-weight: 500 !important;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.section-title {
    margin: 18px 0 3px;
    color: #1F2937;
    font-size: 1.02rem;
    font-weight: 850;
    letter-spacing: -.01em;
}

.section-caption {
    color: #64748B;
    font-size: .72rem;
    margin-bottom: 8px;
}

.panel {
    border: 1px solid var(--line);
    border-radius: 15px;
    background: rgba(9,24,38,.55);
    padding: 4px;
}

.insight {
    border: 1px solid rgba(15,107,120,.20);
    border-left: 3px solid #0F6B78;
    background: #364957;
    border-radius: 10px;
    padding: 10px 12px;
    color: #F5F7FA !important;
    font-size: .78rem;
    font-weight: 500;
    line-height: 1.5;
}

.small-card {
    border: 1px solid var(--line);
    background: rgba(13,28,43,.76);
    border-radius: 13px;
    padding: 12px;
    height: 100%;
}

.small-card-title {
    color: #86a1b4;
    font-size: .67rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: .07em;
}

.small-card-value {
    color: #F5F7FA;
    font-size: 1.15rem;
    font-weight: 850;
    margin-top: 6px;
}

.footer {
    text-align: center;
    color: #64748B;
    font-size: .68rem;
    padding: 18px 0 4px;
}

@media (max-width: 1250px) {
    .kpi-grid { grid-template-columns: repeat(4, minmax(0, 1fr)); }
}
@media (max-width: 760px) {
    .kpi-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .hero { align-items: flex-start; flex-direction: column; min-height: auto; padding: 24px; }
}

div[data-testid="stPlotlyChart"] {
    border: 1px solid rgba(170,205,225,.06);
    border-radius: 14px;
    overflow: hidden;
}

    /* Supplied light professional theme */
    [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div,
    [data-testid="stSidebar"] .stMultiSelect div[data-baseweb="select"] > div,
    [data-testid="stSidebar"] input {
        background: rgba(255,255,255,.08) !important;
        color: #FFFFFF !important;
        border-color: rgba(255,255,255,.16) !important;
    }
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stCaption { color: #FFFFFF !important; }
    [data-testid="stSidebar"] hr { border-color: rgba(255,255,255,.14); }

    /* =========================================================
   RESET FILTER BUTTON
   ========================================================= */

[data-testid="stSidebar"] .reset-filter-btn button {
    width: 100% !important;
    min-height: 40px !important;
    border-radius: 9px !important;
    border: 1px solid rgba(255,255,255,.20) !important;
    background: rgba(255,255,255,.08) !important;
    color: #FFFFFF !important;
    font-size: .78rem !important;
    font-weight: 700 !important;
    transition: all .2s ease !important;
}

[data-testid="stSidebar"] .reset-filter-btn button:hover {
    background: rgba(255,255,255,.16) !important;
    border-color: rgba(255,255,255,.32) !important;
    color: #FFFFFF !important;
}

[data-testid="stSidebar"] .reset-filter-btn button:active {
    transform: scale(.98);
}

</style>"""


def inject_geographic_css():
    """Inject the visual system used by the Geographic & Environmental page."""
    st.markdown(GEOGRAPHIC_CSS, unsafe_allow_html=True)
