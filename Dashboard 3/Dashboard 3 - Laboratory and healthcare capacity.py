import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Laboratory & Healthcare Capacity",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)
# DASHBOARD COLOR PALETTE

PRIMARY_NAVY = "#17324D"
TEAL = "#0F6B78"
SLATE_BLUE = PRIMARY_NAVY
GREEN = "#16855B"
AMBER = "#C98A00"

BACKGROUND = "#F5F7FA"
WHITE = "#FFFFFF"
TEXT = "#1F2937"
SECONDARY_TEXT = "#64748B"
BORDER = "rgba(100, 116, 139, 0.22)"
# DASHBOARD STYLING

st.markdown(f"""
<style>

    /* ================================
       MAIN PAGE
       ================================ */

    .stApp {{
        background-color: {BACKGROUND};
    }}

    /* ==================================================
   STREAMLIT TOP HEADER
   ================================================== */

header[data-testid="stHeader"] {{
    background-color: {BACKGROUND} !important;
    border-bottom: none !important;
}}

/* Header buttons */
header[data-testid="stHeader"] button {{
    color: {PRIMARY_NAVY} !important;
    background-color: transparent !important;
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
}}

/* Header icons */
header[data-testid="stHeader"] button svg {{
    color: {PRIMARY_NAVY} !important;
    fill: {PRIMARY_NAVY} !important;
    stroke: {PRIMARY_NAVY} !important;
}}

/* Deploy button */
header[data-testid="stHeader"] [data-testid="stDeployButton"] {{
    color: {PRIMARY_NAVY} !important;
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
}}

header[data-testid="stHeader"] [data-testid="stDeployButton"] * {{
    color: {PRIMARY_NAVY} !important;
    fill: {PRIMARY_NAVY} !important;
    stroke: {PRIMARY_NAVY} !important;
}}

/* Remove focus outline/border */
header[data-testid="stHeader"] button:focus,
header[data-testid="stHeader"] button:focus-visible {{
    outline: none !important;
    border: none !important;
    box-shadow: none !important;
}}

/* Subtle hover effect */
header[data-testid="stHeader"] button:hover {{
    background-color: rgba(23, 50, 77, 0.06) !important;
}}
    .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
        max-width: 1500px;
    }}


    /* ================================
       TITLE
       ================================ */

    .main-title {{
        font-size: 54px;
        font-weight: 700;
        color: {PRIMARY_NAVY};
        margin-bottom: 5px;
    }}

    .main-subtitle {{
        font-size: 15px;
        color: {SECONDARY_TEXT};
        margin-bottom: 25px;
    }}


    /* ================================
       SECTION HEADINGS
       ================================ */

    h2, h3 {{
        color: {PRIMARY_NAVY} !important;
        font-weight: 650 !important;
    }}


    /* ================================
       SIDEBAR
       ================================ */

    section[data-testid="stSidebar"] {{
        background-color: {BACKGROUND};
        border-right: 1px solid {BORDER};
    }}

    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {{
        color: {PRIMARY_NAVY} !important;
    }}

    section[data-testid="stSidebar"] label {{
        color: {TEXT} !important;
        font-weight: 500;
    }}


    /* ================================
       FILTER BOXES
       ================================ */

    div[data-baseweb="select"] > div {{
        border-radius: 8px;
        border-color: {BORDER};
    }}


    /* ==================================================
   KPI CARDS - FORCE TEXT VISIBILITY
   ================================================== */

div[data-testid="stMetric"] {{
    background-color: {WHITE} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 12px !important;
    padding: 14px 16px !important;
    box-shadow: 0 2px 8px rgba(18, 53, 91, 0.06) !important;
    min-height: 105px !important;
    box-sizing: border-box !important;
}}

/* KPI LABEL */
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

/* KPI VALUE */
div[data-testid="stMetricValue"],
div[data-testid="stMetricValue"] *,
[data-testid="stMetricValue"] div,
[data-testid="stMetricValue"] span {{
    color: {PRIMARY_NAVY} !important;
    opacity: 1 !important;
    visibility: visible !important;
    -webkit-text-fill-color: {PRIMARY_NAVY} !important;
    font-size: 25px !important;
    font-weight: 700 !important;
}}

    /* Prevent faded text inside metric cards */
div[data-testid="stMetric"] p {{
    opacity: 1 !important;
    color: {TEXT} !important;
}}


    /* ================================
       CHART CONTAINERS
       ================================ */

    div[data-testid="stPlotlyChart"] {{
        background-color: {WHITE};
        border: 1px solid {BORDER};
        border-radius: 12px;
        padding: 10px;
        box-shadow: 0 2px 8px rgba(18, 53, 91, 0.05);
    }}


    /* ================================
       EXPANDER / DATA TABLE CARD STYLE
       (MATCHING TEAL ACCENT CALLOUT STYLE)
       ================================ */

    div[data-testid="stExpander"] {{
        background-color: {WHITE} !important;
        border: 1px solid {BORDER} !important;
        border-left: 4px solid {TEAL} !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 8px rgba(18, 53, 91, 0.05) !important;
        margin-top: 20px !important;
        margin-bottom: 20px !important;
        overflow: hidden !important;
    }}

    div[data-testid="stExpander"] summary,
    div[data-testid="stExpander"] summary * {{
        font-weight: 650 !important;
        color: {PRIMARY_NAVY} !important;
        font-size: 1.25rem !important;
    }}

    div[data-testid="stExpander"] summary:hover,
    div[data-testid="stExpander"] summary:hover * {{
        color: {TEAL} !important;
    }}

</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="main-title">Laboratory & Healthcare Capacity</div>',
    unsafe_allow_html=True
)


# 1. LOAD & MERGE DATA (cached so it only runs once,
#    not on every filter interaction)

@st.cache_data
def load_data():
    fact = pd.read_csv("fact_lab_healthcare_cleaned.csv")
    dates = pd.read_csv("dim_dates_cleaned.csv")
    states = pd.read_csv("dim_state_cleaned.csv")

    df = fact.merge(
        dates[["date_id", "year", "month_num", "month_name", "year_month"]],
        on="date_id",
        how="left"
    )

    df = df.merge(
        states[["state_id", "state_name"]],
        on="state_id",
        how="left"
    )

    # Merges can upcast year to float (e.g. 2021.0); keep it a clean int
    df["year"] = df["year"].astype("Int64")

    return df


try:
    df = load_data()
except FileNotFoundError as e:
    st.error(
        f"⚠️ Required data file not found: {e}. "
        "Make sure fact_lab_healthcare_cleaned.csv, dim_dates_cleaned.csv, "
        "and dim_state_cleaned.csv are in the app directory."
    )
    st.stop()

# Subtitle: quick context on coverage of the underlying dataset
n_states = df["state_name"].nunique()
date_min = df["year_month"].min()
date_max = df["year_month"].max()

st.markdown(
    f'<div class="main-subtitle">Covering {n_states} states · '
    f'{date_min} to {date_max}</div>',
    unsafe_allow_html=True
)


# 2. SIDEBAR BRANDING

st.sidebar.markdown(
    """
    <div style="text-align:center; margin-bottom:10px;">
        <span style="font-size:40px;">🏥</span>
    </div>
    """,
    unsafe_allow_html=True
)


# 3. FILTERS

st.sidebar.markdown(
    """
    <h2 style="
        color:#17324D;
        margin-bottom:5px;
    ">
        Dashboard Filters
    </h2>
    """,
    unsafe_allow_html=True
)

st.sidebar.caption(
    "Select the required filters to update the dashboard."
)

# Initialize Session State for filters if not set
if "state_filter" not in st.session_state:
    st.session_state["state_filter"] = "All"
if "year_filter" not in st.session_state:
    st.session_state["year_filter"] = "All"
if "month_filter" not in st.session_state:
    st.session_state["month_filter"] = "All"

def reset_filters():
    st.session_state["state_filter"] = "All"
    st.session_state["year_filter"] = "All"
    st.session_state["month_filter"] = "All"

# Reset filters button
st.sidebar.button("↺ Reset Filters", on_click=reset_filters, use_container_width=True)

# State
state_options = ["All"] + sorted(
    df["state_name"].dropna().unique().tolist()
)

selected_state = st.sidebar.selectbox(
    "State",
    state_options,
    key="state_filter"
)

# Year
year_options = ["All"] + sorted(
    df["year"].dropna().unique().tolist()
)

selected_year = st.sidebar.selectbox(
    "Year",
    year_options,
    key="year_filter"
)

# Month
month_options = ["All"] + df[
    ["month_num", "month_name"]
].drop_duplicates().sort_values(
    "month_num"
)["month_name"].tolist()

selected_month = st.sidebar.selectbox(
    "Month",
    month_options,
    key="month_filter"
)


# 4. APPLY FILTERS

filtered_df = df.copy()

if selected_state != "All":
    filtered_df = filtered_df[
        filtered_df["state_name"] == selected_state
    ]

if selected_year != "All":
    filtered_df = filtered_df[
        filtered_df["year"] == selected_year
    ]

if selected_month != "All":
    filtered_df = filtered_df[
        filtered_df["month_name"] == selected_month
    ]

# Guard against empty dataset
if filtered_df.empty:
    st.warning("⚠️ **No data available for the selected filter combination.** Please adjust or reset your State, Year, or Month selections.")
    st.stop()

# Download filtered data
st.sidebar.markdown("---")
st.sidebar.download_button(
    label="⬇ Download Filtered Data (CSV)",
    data=filtered_df.to_csv(index=False).encode("utf-8"),
    file_name="filtered_lab_healthcare_data.csv",
    mime="text/csv"
)


# 5. KPI CALCULATIONS & DELTAS

total_tests = filtered_df["total_tests"].sum()

positive_tests = filtered_df["positive_tests"].sum()

if total_tests > 0:
    positivity_rate = (
        positive_tests / total_tests
    ) * 100
else:
    positivity_rate = 0

vaccination_coverage = (
    filtered_df["vaccination_coverage_pct"].mean()
)

booster_coverage = (
    filtered_df["booster_coverage_pct"].mean()
)

hospital_beds = (
    filtered_df["hospital_beds"].sum()
)

doctors = (
    filtered_df["doctors"].sum()
)

icu_utilization = (
    filtered_df["icu_utilization_pct"].mean()
)

reporting_compliance = (
    filtered_df["reporting_compliance_pct"].mean()
)

# Determine ICU Utilization Status & Colors
# >85: ALERT (red text), 50-85: MODERATE, <50: NORMAL
def icu_status_color(value):
    """Single source of truth for ICU status thresholds/colors —
    used by both the KPI card and the ICU gauge chart."""
    if value > 85:
        return "ALERT", "#D9381E", "rgba(217, 56, 30, 0.12)"        # Bold Red
    elif value >= 50:
        return "MODERATE", "#C98A00", "rgba(201, 138, 0, 0.12)"     # Amber / Orange
    else:
        return "NORMAL", "#16855B", "rgba(22, 133, 91, 0.12)"       # Green

icu_status, icu_color, icu_bg_color = icu_status_color(icu_utilization)

# Config for Month-over-Month (MoM) KPI deltas:
# key -> (column, aggregation, kind)
#   kind="pct_of_prev"  -> % change relative to previous month's value (sums)
#   kind="pp_diff"      -> plain point difference (percentages/rates, means)
#   kind="ratio_pp"     -> point difference of a computed ratio (positivity rate)
_DELTA_METRICS = {
    "total_tests":          ("total_tests", "sum", "pct_of_prev"),
    "positive_tests":       ("positive_tests", "sum", "pct_of_prev"),
    "vaccination_coverage": ("vaccination_coverage_pct", "mean", "pp_diff"),
    "booster_coverage":     ("booster_coverage_pct", "mean", "pp_diff"),
    "hospital_beds":        ("hospital_beds", "sum", "pct_of_prev"),
    "doctors":               ("doctors", "sum", "pct_of_prev"),
    "icu_utilization":       ("icu_utilization_pct", "mean", "pp_diff"),
    "reporting_compliance":  ("reporting_compliance_pct", "mean", "pp_diff"),
}

def calculate_kpi_deltas(current_filtered, full_dataset, state_sel):
    """Compute Month-over-Month deltas for each KPI, comparing the latest
    month in the current filter selection to the prior month (within the
    same state scope, ignoring the year/month filters so there's always
    something to compare against)."""
    ref_df = full_dataset if state_sel == "All" else full_dataset[full_dataset["state_name"] == state_sel]

    unique_ym = sorted(current_filtered["year_month"].unique())
    if not unique_ym:
        return {}

    latest_ym = unique_ym[-1]
    all_ym = sorted(ref_df["year_month"].unique())
    idx = all_ym.index(latest_ym) if latest_ym in all_ym else -1
    prev_ym = all_ym[idx - 1] if idx > 0 else None

    cur_df = current_filtered[current_filtered["year_month"] == latest_ym]
    prev_df = ref_df[ref_df["year_month"] == prev_ym] if prev_ym else pd.DataFrame()

    deltas = {}
    for key, (col, agg, kind) in _DELTA_METRICS.items():
        cur_val = getattr(cur_df[col], agg)()
        prev_val = getattr(prev_df[col], agg)() if not prev_df.empty else 0

        if kind == "pct_of_prev":
            deltas[key] = f"{((cur_val - prev_val) / prev_val) * 100:+.1f}% MoM" if prev_val > 0 else None
        else:  # pp_diff
            deltas[key] = f"{(cur_val - prev_val):+.2f}% MoM" if not prev_df.empty else None

    # Positivity Rate is a derived ratio, computed separately
    tot_cur = cur_df["total_tests"].sum()
    tot_prev = prev_df["total_tests"].sum() if not prev_df.empty else 0
    pos_cur = cur_df["positive_tests"].sum()
    pos_prev = prev_df["positive_tests"].sum() if not prev_df.empty else 0
    pr_cur = (pos_cur / tot_cur * 100) if tot_cur > 0 else 0
    pr_prev = (pos_prev / tot_prev * 100) if tot_prev > 0 else 0
    deltas["positivity_rate"] = f"{(pr_cur - pr_prev):+.2f}% MoM" if tot_prev > 0 else None

    return deltas

deltas = calculate_kpi_deltas(filtered_df, df, selected_state)


# 5b. INSIGHT CALLOUT

_insight_bits = []

_pos_delta = deltas.get("positivity_rate")
if _pos_delta:
    direction = "up" if _pos_delta.startswith("+") else "down"
    _insight_bits.append(f"Positivity rate is {direction} {_pos_delta.lstrip('+-')} this month")

_insight_bits.append(f"ICU utilization is **{icu_status}** at {icu_utilization:.1f}%")

_scope = selected_state if selected_state != "All" else "across all states"
_insight_text = f"📌 {'; '.join(_insight_bits)} ({_scope})."

st.markdown(
    f"""
    <div style="
        background-color: {WHITE};
        border-left: 4px solid {TEAL};
        border-radius: 8px;
        padding: 12px 18px;
        margin-bottom: 20px;
        font-size: 14px;
        color: {TEXT};
        box-shadow: 0 2px 8px rgba(18, 53, 91, 0.05);
    ">
        {_insight_text}
    </div>
    """,
    unsafe_allow_html=True
)


# 6. KPI DISPLAY

st.markdown(
    '<h2 style="margin-top:10px; margin-bottom:18px;">'
    'Key Performance Indicators'
    '</h2>',
    unsafe_allow_html=True
)

row1 = st.columns(5)

row1[0].metric(
    "Total Tests",
    f"{total_tests:,.0f}",
    delta=deltas.get("total_tests")
)

row1[1].metric(
    "Positive Tests",
    f"{positive_tests:,.0f}",
    delta=deltas.get("positive_tests")
)

row1[2].metric(
    "Positivity Rate",
    f"{positivity_rate:.2f}%",
    delta=deltas.get("positivity_rate"),
    delta_color="inverse"
)

row1[3].metric(
    "Vaccination Coverage",
    f"{vaccination_coverage:.2f}%",
    delta=deltas.get("vaccination_coverage")
)

row1[4].metric(
    "Booster Coverage",
    f"{booster_coverage:.2f}%",
    delta=deltas.get("booster_coverage")
)


row2 = st.columns(4)

row2[0].metric(
    "Hospital Beds",
    f"{hospital_beds:,.0f}",
    delta=deltas.get("hospital_beds")
)

row2[1].metric(
    "Doctors",
    f"{doctors:,.0f}",
    delta=deltas.get("doctors")
)

# ICU Utilization Card with dynamic alert status badge
icu_mom = f" <span style='font-size: 12px; color: #64748B;'>({deltas.get('icu_utilization')})</span>" if deltas.get('icu_utilization') else ""

row2[2].markdown(
    f"""
    <div style="
        background-color: #FFFFFF;
        border: 1px solid rgba(100, 116, 139, 0.22);
        border-radius: 12px;
        padding: 14px 16px;
        box-shadow: 0 2px 8px rgba(18, 53, 91, 0.06);
        min-height: 105px;
        box-sizing: border-box;
        width: 100%;
        overflow: hidden;
    ">
        <div style="font-size: 13px; font-weight: 600; color: #1F2937; margin-bottom: 6px; display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 4px;">
            <span style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">ICU Utilization</span>
            <span style="background-color: {icu_bg_color}; color: {icu_color}; padding: 2px 8px; border-radius: 6px; font-size: 11px; font-weight: 700; border: 1px solid {icu_color}40; white-space: nowrap; flex-shrink: 0; margin-left: auto;">
                {icu_status}
            </span>
        </div>
        <div style="font-size: 25px; font-weight: 700; color: #17324D; white-space: nowrap;">
            {icu_utilization:.2f}%{icu_mom}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

row2[3].metric(
    "Reporting Compliance",
    f"{reporting_compliance:.2f}%",
    delta=deltas.get("reporting_compliance")
)

# TESTING TREND + VACCINATION PROGRESS
# SIDE-BY-SIDE LAYOUT

col1, col2 = st.columns(2)

# ==================================================
# VISUAL 1 - TESTING TREND
# ==================================================

with col1:

    st.subheader("Testing Trend")

    monthly_testing = (
        filtered_df
        .groupby("year_month", as_index=False)
        .agg(
            total_tests=("total_tests", "sum"),
            positive_tests=("positive_tests", "sum")
        )
        .sort_values("year_month")
    )

    fig_testing = go.Figure()

    fig_testing.add_trace(
        go.Scatter(
            x=monthly_testing["year_month"],
            y=monthly_testing["total_tests"],
            mode="lines",
            name="Total Tests",
            line=dict(
                color=PRIMARY_NAVY,
                width=3
            ),
            hovertemplate=(
                "Month: %{x}<br>"
                "Total Tests: %{y:,.0f}"
                "<extra></extra>"
            )
        )
    )

    fig_testing.add_trace(
        go.Scatter(
            x=monthly_testing["year_month"],
            y=monthly_testing["positive_tests"],
            mode="lines",
            name="Positive Tests",
            line=dict(
                color=TEAL,
                width=3
            ),
            hovertemplate=(
                "Month: %{x}<br>"
                "Positive Tests: %{y:,.0f}"
                "<extra></extra>"
            )
        )
    )

    fig_testing.update_layout(
        xaxis_title=dict(
            text="Month",
            font=dict(
                color=TEXT,
                size=13
            )
        ),
        yaxis_title=dict(
            text="Tests",
            font=dict(
                color=TEXT,
                size=13
            )
        ),
        hovermode="x unified",
        plot_bgcolor=WHITE,
        paper_bgcolor=WHITE,
        font=dict(
            family="Arial",
            color=TEXT,
            size=11
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(
                color=TEXT,
                size=10
            )
        ),
        margin=dict(
            l=50,
            r=20,
            t=55,
            b=45
        )
    )

    fig_testing.update_xaxes(
        showgrid=False,
        linecolor=BORDER,
        tickfont=dict(
            color=TEXT,
            size=9
        )
    )

    fig_testing.update_yaxes(
        showgrid=True,
        gridcolor="rgba(100, 116, 139, 0.12)",
        zeroline=False,
        linecolor=BORDER,
        tickfont=dict(
            color=TEXT,
            size=9
        )
    )

    st.plotly_chart(
        fig_testing,
        use_container_width=True
    )


# ==================================================
# VISUAL 2 - VACCINATION PROGRESS
# ==================================================

with col2:

    st.subheader("Vaccination Progress")

    monthly_vaccination = (
        filtered_df
        .groupby("year_month", as_index=False)
        .agg(
            vaccination_coverage=(
                "vaccination_coverage_pct",
                "mean"
            ),
            booster_coverage=(
                "booster_coverage_pct",
                "mean"
            )
        )
        .sort_values("year_month")
    )

    fig_vaccination = go.Figure()

    fig_vaccination.add_trace(
        go.Scatter(
            x=monthly_vaccination["year_month"],
            y=monthly_vaccination["vaccination_coverage"],
            mode="lines",
            name="Vaccination Coverage",
            line=dict(
                color=TEAL,
                width=3
            ),
            fill="tozeroy",
            fillcolor="rgba(15, 107, 120, 0.18)",
            hovertemplate=(
                "Month: %{x}<br>"
                "Vaccination Coverage: %{y:.2f}%"
                "<extra></extra>"
            )
        )
    )

    fig_vaccination.add_trace(
        go.Scatter(
            x=monthly_vaccination["year_month"],
            y=monthly_vaccination["booster_coverage"],
            mode="lines",
            name="Booster Coverage",
            line=dict(
                color=GREEN,
                width=3
            ),
            fill="tozeroy",
            fillcolor="rgba(22, 133, 91, 0.18)",
            hovertemplate=(
                "Month: %{x}<br>"
                "Booster Coverage: %{y:.2f}%"
                "<extra></extra>"
            )
        )
    )

    fig_vaccination.update_layout(
        xaxis_title=dict(
            text="Month",
            font=dict(
                color=TEXT,
                size=13
            )
        ),
        yaxis_title=dict(
            text="Coverage (%)",
            font=dict(
                color=TEXT,
                size=13
            )
        ),
        hovermode="x unified",
        plot_bgcolor=WHITE,
        paper_bgcolor=WHITE,
        font=dict(
            family="Arial",
            color=TEXT,
            size=11
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(
                color=TEXT,
                size=10
            )
        ),
        margin=dict(
            l=50,
            r=20,
            t=55,
            b=45
        )
    )

    fig_vaccination.update_xaxes(
        showgrid=False,
        linecolor=BORDER,
        tickfont=dict(
            color=TEXT,
            size=9
        )
    )

    fig_vaccination.update_yaxes(
        showgrid=True,
        gridcolor="rgba(100, 116, 139, 0.12)",
        zeroline=False,
        linecolor=BORDER,
        tickfont=dict(
            color=TEXT,
            size=9
        ),
        range=[0, 100]
    )

    st.plotly_chart(
        fig_vaccination,
        use_container_width=True
    )

# HOSPITAL CAPACITY + ICU UTILIZATION +
# LABORATORY PERFORMANCE
# SIDE-BY-SIDE LAYOUT

col3, col4, col5 = st.columns(3)


# ==================================================
# VISUAL 3 - HOSPITAL CAPACITY
# ==================================================

with col3:

    st.subheader("Hospital Capacity")

    hospital_capacity = pd.DataFrame({
        "Category": [
            "Hospital Beds",
            "Doctors",
            "PHCs",
            "CHCs"
        ],
        "Value": [
            filtered_df["hospital_beds"].sum(),
            filtered_df["doctors"].sum(),
            filtered_df["phc_count"].sum(),
            filtered_df["chc_count"].sum()
        ]
    })

    fig_capacity = go.Figure()

    fig_capacity.add_trace(
        go.Bar(
            x=hospital_capacity["Category"],
            y=hospital_capacity["Value"],
            text=hospital_capacity["Value"],
            texttemplate="%{text:,.0f}",
            textposition="outside",
            name="Capacity",
            marker_color=SLATE_BLUE,
            hovertemplate=(
                "%{x}<br>"
                "Value: %{y:,.0f}"
                "<extra></extra>"
            )
        )
    )

    fig_capacity.update_layout(
        height=390,
        xaxis_title="",
        yaxis_title="Count",
        plot_bgcolor=WHITE,
        paper_bgcolor=WHITE,
        font=dict(
            family="Arial",
            color=TEXT,
            size=10
        ),
        showlegend=False,
        margin=dict(
            l=45,
            r=15,
            t=30,
            b=70
        )
    )

    fig_capacity.update_xaxes(
        tickfont=dict(
            color=TEXT,
            size=9
        ),
        showgrid=False
    )

    fig_capacity.update_yaxes(
        tickfont=dict(
            color=TEXT,
            size=9
        ),
        showgrid=True,
        gridcolor="rgba(100, 116, 139, 0.12)"
    )

    st.plotly_chart(
        fig_capacity,
        use_container_width=True
    )


# ==================================================
# VISUAL 4 - ICU UTILIZATION
# ==================================================

with col4:

    st.subheader("ICU Utilization")

    icu_value = filtered_df[
        "icu_utilization_pct"
    ].mean()

    gauge_status, gauge_color, _ = icu_status_color(icu_value)

    fig_icu = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=icu_value,

            number=dict(
                suffix="%",
                valueformat=".2f",
                font=dict(
                    color=PRIMARY_NAVY,
                    size=36,
                    family="Arial"
                )
            ),

            gauge=dict(
                axis=dict(
                    range=[0, 100],
                    tickwidth=1,
                    tickcolor="rgba(100, 116, 139, 0.3)",
                    tickfont=dict(
                        color=TEXT,
                        size=10
                    )
                ),

                bar=dict(
                    color=gauge_color,
                    thickness=0.28
                ),

                bgcolor=WHITE,

                bordercolor=BORDER,
                borderwidth=1,

                steps=[
                    {'range': [0, 50], 'color': "rgba(22, 133, 91, 0.10)"},
                    {'range': [50, 85], 'color': "rgba(201, 138, 0, 0.10)"},
                    {'range': [85, 100], 'color': "rgba(217, 56, 30, 0.14)"}
                ],

                threshold=dict(
                    line=dict(color="#D9381E", width=3),
                    thickness=0.75,
                    value=85
                )
            ),

            title=dict(
                text=f"<b style='color:{gauge_color}; font-size:22px;'>{gauge_status}</b><br><span style='color:#64748B; font-size:13px;'>ICU Utilization Status</span>",
                font=dict(
                    family="Arial"
                )
            )
        )
    )

    fig_icu.update_layout(
        height=390,
        plot_bgcolor=WHITE,
        paper_bgcolor=WHITE,
        font=dict(
            family="Arial",
            color=TEXT
        ),
        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20
        )
    )

    st.plotly_chart(
        fig_icu,
        use_container_width=True
    )


# ==================================================
# VISUAL 5 - LABORATORY PERFORMANCE
# ==================================================

with col5:

    st.subheader("Laboratory Performance")

    reporting_rate = filtered_df[
        "reporting_rate_pct"
    ].mean()

    turnaround_time = filtered_df[
        "turnaround_time_days"
    ].mean()

    laboratory_performance = pd.DataFrame({
        "Metric": [
            "Reporting Rate",
            "Turnaround Time"
        ],
        "Value": [
            reporting_rate,
            turnaround_time
        ]
    })

    fig_lab = go.Figure()

    fig_lab.add_trace(
        go.Bar(
            x=laboratory_performance["Metric"],
            y=laboratory_performance["Value"],
            text=laboratory_performance["Value"],
            texttemplate="%{text:.2f}",
            textposition="outside",
            name="Laboratory Performance",
            marker_color=TEAL,
            hovertemplate=(
                "%{x}<br>"
                "Value: %{y:.2f}"
                "<extra></extra>"
            )
        )
    )

    fig_lab.update_layout(
        height=390,
        xaxis_title="",
        yaxis_title="Value",
        plot_bgcolor=WHITE,
        paper_bgcolor=WHITE,
        font=dict(
            family="Arial",
            color=TEXT,
            size=10
        ),
        showlegend=False,
        margin=dict(
            l=45,
            r=15,
            t=30,
            b=70
        )
    )

    fig_lab.update_xaxes(
        tickfont=dict(
            color=TEXT,
            size=9
        ),
        showgrid=False
    )

    fig_lab.update_yaxes(
        tickfont=dict(
            color=TEXT,
            size=9
        ),
        showgrid=True,
        gridcolor="rgba(100, 116, 139, 0.12)"
    )

    st.plotly_chart(
        fig_lab,
        use_container_width=True
    )
# VISUAL 6 - BED OCCUPANCY HEAT MAP

st.subheader("Bed Occupancy by State")

# Calculate average bed occupancy for each State and Month
bed_occupancy = (
    filtered_df
    .groupby(
        ["state_name", "year_month"],
        as_index=False
    )
    .agg(
        bed_occupancy=("bed_occupancy_pct", "mean")
    )
)

# Create State × Month matrix
heatmap_data = bed_occupancy.pivot(
    index="state_name",
    columns="year_month",
    values="bed_occupancy"
)

# Sort states alphabetically
heatmap_data = heatmap_data.sort_index()

# Sort months chronologically
heatmap_data = heatmap_data.reindex(
    sorted(heatmap_data.columns),
    axis=1
)

fig_bed = go.Figure(
    data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,

    colorscale=[
        [0.0, "#E7F2F4"],   # Low occupancy → light
        [0.5, "#73AAB3"],   # Medium occupancy
        [1.0, "#0F6B78"]    # High occupancy → dark
    ],

        colorbar=dict(
            title="Occupancy (%)"
        ),

        hovertemplate=(
            "State: %{y}<br>"
            "Month: %{x}<br>"
            "Bed Occupancy: %{z:.2f}%"
            "<extra></extra>"
        ),

        xgap=1,
        ygap=1
    )
)

fig_bed.update_layout(
    height=650,

    plot_bgcolor=WHITE,
    paper_bgcolor=WHITE,

    font=dict(
        family="Arial",
        color=TEXT,
        size=11
    ),

    xaxis=dict(
        title="Month",
        title_font=dict(
            color=TEXT,
            size=14
        ),
        tickfont=dict(
            color=TEXT,
            size=10
        ),
        showgrid=False,
        side="bottom"
    ),

    yaxis=dict(
        title="State",
        title_font=dict(
            color=TEXT,
            size=14
        ),
        tickfont=dict(
            color=TEXT,
            size=10
        ),
        showgrid=False,
        autorange="reversed"
    ),

    margin=dict(
        l=120,
        r=80,
        t=40,
        b=70
    )
)

st.plotly_chart(
    fig_bed,
    use_container_width=True
)


# 7. FILTERED DATA DETAILS TABLE

with st.expander("📋 View & Explore Filtered Data Table", expanded=False):
    st.markdown("<h4 style='color:#17324D; margin-top:5px; margin-bottom:10px;'>Detailed Operations Breakdown</h4>", unsafe_allow_html=True)
    display_cols = [
        "state_name", "year_month", "total_tests", "positive_tests",
        "vaccination_coverage_pct", "booster_coverage_pct",
        "hospital_beds", "doctors", "icu_utilization_pct", "reporting_compliance_pct"
    ]
    available_cols = [c for c in display_cols if c in filtered_df.columns]
    rename_map = {
        "state_name": "State",
        "year_month": "Month",
        "total_tests": "Total Tests",
        "positive_tests": "Positive Tests",
        "vaccination_coverage_pct": "Vaccination (%)",
        "booster_coverage_pct": "Booster (%)",
        "hospital_beds": "Hospital Beds",
        "doctors": "Doctors",
        "icu_utilization_pct": "ICU Util (%)",
        "reporting_compliance_pct": "Compliance (%)"
    }
    st.dataframe(
        filtered_df[available_cols].rename(columns=rename_map),
        use_container_width=True,
        hide_index=True
    )


# 8. FOOTER

st.markdown(
    f"""
    <div style="
        margin-top: 30px;
        padding-top: 15px;
        border-top: 1px solid {BORDER};
        text-align: center;
        font-size: 12px;
        color: {SECONDARY_TEXT};
    ">
        Source: Laboratory & Healthcare Capacity dataset · Data range: {date_min} to {date_max} ·
    </div>
    """,
    unsafe_allow_html=True
)