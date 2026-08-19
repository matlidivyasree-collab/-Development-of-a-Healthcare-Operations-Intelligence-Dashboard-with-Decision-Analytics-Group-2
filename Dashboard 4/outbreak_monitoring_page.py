import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

from chart_config import (
    load_css, page_header, chart_title, kpi, insight, fmt, fmt_pct,
    COLORS, COLOR_SEQUENCE, chart_cfg
)
from pdf_export import render_pdf_button

ALERT_ORDER = {"High": 3, "Moderate": 2, "Low": 1}


# ── LOAD DATA ───
@st.cache_data
def load_data():
    """Load cleaned outbreak records, dimensions, and ARIMA forecast outputs."""
    df = pd.read_csv("cleaning/fact_outbreak_clean.csv")
    dim_date = pd.read_csv("data/dim_date.csv")
    dim_state = pd.read_csv("data/dim_state.csv")
    dim_disease = pd.read_csv("data/dim_disease.csv")

    # Star-schema joins.
    # NOTE: the cleaned fact table already carries a denormalised state_name;
    # drop it first so the merge with dim_state does not rename it to state_name_x/y.
    if "state_name" in df.columns:
        df = df.drop(columns=["state_name"])
    df = df.merge(dim_date[["date_id", "full_date", "year", "year_month", "month_name"]],
                  on="date_id", how="left")
    df = df.merge(dim_state[["state_id", "state_name", "region"]], on="state_id", how="left")
    df = df.merge(dim_disease[["disease_id", "disease_name", "disease_category"]],
                  on="disease_id", how="left")

    df["full_date"] = pd.to_datetime(df["full_date"], errors="coerce")
    df["year_month"] = df["year_month"].astype(str)
    df["region"] = df["region"].astype(str).str.strip()   # fix "East " style dirt
    for c in ["new_outbreak_flag", "controlled_flag", "emergency_alert_flag"]:
        df[c] = df[c].astype(bool)

    history = pd.read_csv("data/monthly_outbreak_history.csv")
    history["Month"] = pd.to_datetime(history["Month"], errors="coerce")

    forecast = pd.read_csv("data/outbreak_forecast.csv")
    forecast["Month"] = pd.to_datetime(forecast["Month"], errors="coerce")

    return df, history, forecast


# ── SIDEBAR FILTERS (applied from app.py's filter bar) 
def apply_filters(df) -> pd.DataFrame:
    """
    Apply the sidebar filter bar (Year | State | Region | Disease | Alert | Date).
    """
    f = st.session_state.get("filters", {})

    years    = f.get("year")        or sorted(df["year"].unique().tolist())
    states   = f.get("state")       or sorted(df["state_name"].unique().tolist())
    regions  = f.get("region")      or sorted(df["region"].unique().tolist())
    diseases = f.get("disease")     or sorted(df["disease_name"].unique().tolist())
    alerts   = f.get("alert_level") or sorted(df["alert_level"].unique().tolist())
    date_range = f.get("date_range")

    mask = (
        df["year"].isin(years)
        & df["state_name"].isin(states)
        & df["region"].isin(regions)
        & df["disease_name"].isin(diseases)
        & df["alert_level"].isin(alerts)
    )
    if date_range is not None:
        if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
            start, end = date_range
        else:                                   # single date picked
            start = end = date_range
        mask &= df["full_date"].dt.date.between(start, end)

    filtered = df[mask]
    if filtered.empty:
        st.warning("⚠️ No records match the current sidebar filters — showing all data instead.")
        return df

    n = len(filtered)
    # st.caption(
    #     f"🎯 Sidebar filters active — showing **{n:,}** of **{len(df):,}** outbreak records · "
    #     f"{filtered['state_name'].nunique()} states · {filtered['disease_name'].nunique()} diseases · "
    #     f"{filtered['year'].nunique()} years"
    # )
    return filtered


def new_outbreak_count(df_f) -> int:
    """New outbreaks = records in the most recent calendar month of the filtered data.

    The raw source's new_outbreak_flag is constant True (data-quality issue), so 'new'
    is derived from time instead: the latest year_month present in the current view.
    """
    if df_f.empty:
        return 0
    latest = df_f["year_month"].max()
    return int((df_f["year_month"] == latest).sum())


def latest_month_label(df_f) -> str:
    """Short label of the latest month in the filtered data, e.g. 'Dec 2024'."""
    latest = df_f["year_month"].max()
    y, m = latest.split("-")
    return datetime(int(y), int(m), 1).strftime("%b %Y")


# ── TOP GROUPS (static bar charts) ──
def top_groups_chart(df, group_col: str, top_n: int = 10):
    """
    Static horizontal bar chart: top-N groups by total historical cases.
    (Replaces the old animated bar-race — same insight, no animation.)
    """
    g = df.groupby(group_col)["historical_cases"].sum().nlargest(top_n).reset_index()
    g = g.sort_values("historical_cases")
    fig = go.Figure(go.Bar(
        x=g["historical_cases"], y=g[group_col], orientation="h",
        marker=dict(
            color=g["historical_cases"],
            colorscale=[[0, COLORS["cyan"]], [0.5, COLORS["gold"]], [1, COLORS["red"]]],
            line=dict(color="rgba(2,8,23,0.6)", width=1),
            showscale=False,
        ),
        text=[f"{int(v):,}" for v in g["historical_cases"]], textposition="auto",
    ))
    fig.update_layout(**chart_cfg(xlabel="Total Cases", ylabel=""))
    # y-axis fix: never show the raw column name (state_name / disease_name);
    # automargin lets the group labels fit.
    fig.update_yaxes(title=None, automargin=True)
    fig.update_layout(margin=dict(l=140, r=24, t=20, b=30))
    fig.update_layout(hovermode="closest", showlegend=False)
    return fig


# ── MONITORING CHARTS (filtered fact data) 
def monthly_trend_chart(df_f):
    """Month → number of outbreak events (monitoring trend)."""
    m = df_f.groupby("year_month").size().reset_index(name="outbreaks").sort_values("year_month")
    fig = go.Figure(go.Scatter(
        x=m["year_month"], y=m["outbreaks"], mode="lines+markers",
        line=dict(color=COLORS["gold"], width=2.5),
        marker=dict(size=6), fill="tozeroy", fillcolor="rgba(255,215,0,0.10)",
    ))
    fig.update_layout(**chart_cfg(xlabel="Month", ylabel="Outbreak Events"))
    fig.update_xaxes(tickangle=45)
    return fig


def alert_level_chart(df_f):
    """Alert distribution sorted logically High → Moderate → Low."""
    counts = df_f["alert_level"].value_counts().reindex(["High", "Moderate", "Low"]).fillna(0)
    fig = go.Figure(data=[go.Pie(
        labels=counts.index, values=counts.values,
        marker=dict(colors=[COLORS["red"], COLORS["orange"], COLORS["green"]]),
        hole=0.5, textinfo="label+percent",
    )])
    fig.update_layout(**chart_cfg())
    fig.update_layout(showlegend=False)
    return fig


def severity_funnel(df_f):
    """Outbreak severity funnel: Total → New → Emergency → Controlled."""
    stages = {
        "Total Outbreaks": len(df_f),
        "New Outbreaks": new_outbreak_count(df_f),
        "Emergency Alerts": int(df_f["emergency_alert_flag"].sum()),
        "Controlled": int(df_f["controlled_flag"].sum()),
    }
    fig = go.Figure(go.Funnel(
        y=list(stages.keys()), x=list(stages.values()),
        textinfo="value+percent initial",
        marker=dict(color=[COLORS["cyan"], COLORS["gold"], COLORS["red"], COLORS["green"]]),
        textfont=dict(color="#0F172A", size=12),
    ))
    fig.update_layout(**chart_cfg())
    fig.update_layout(showlegend=False)
    return fig


def response_time_chart(df_f):
    fig = go.Figure(data=[go.Histogram(
        x=df_f["response_time_hours"], nbinsx=25,
        marker=dict(color=COLORS["cyan"], line=dict(color=COLORS["dark_blue"], width=0.5)),
        opacity=0.85,
    )])
    fig.update_layout(**chart_cfg(xlabel="Response Time (hours)", ylabel="Outbreaks"))
    return fig


# ── FORECASTING CHARTS ────
def historical_forecast_chart(history, forecast):
    """ARIMA national trend: historical + 6-month forecast, with rangeslider."""
    history_plot = history.copy(); history_plot["Type"] = "Historical"
    forecast_plot = forecast.rename(columns={"Forecast_Cases": "Actual_Cases"}).copy()
    forecast_plot["Type"] = "Forecast"
    combined = pd.concat([history_plot, forecast_plot], ignore_index=True)

    fig = go.Figure()
    hist_part = combined[combined["Type"] == "Historical"]
    fcst_part = combined[combined["Type"] == "Forecast"]
    fig.add_trace(go.Scatter(
        x=hist_part["Month"], y=hist_part["Actual_Cases"],
        mode="lines+markers", name="Historical",
        line=dict(color=COLORS["gold"], width=2.5), marker=dict(size=6),
        fill="tozeroy", fillcolor="rgba(255,215,0,0.1)",
    ))
    fig.add_trace(go.Scatter(
        x=fcst_part["Month"], y=fcst_part["Actual_Cases"],
        mode="lines+markers", name="Forecast (6-month)",
        line=dict(color=COLORS["cyan"], width=2.5, dash="dash"),
        marker=dict(size=7, symbol="diamond"), fill="tozeroy",
        fillcolor="rgba(0,229,255,0.05)",
    ))
    fig.update_layout(**chart_cfg(xlabel="Month", ylabel="Cases"))
    fig.update_xaxes(rangeslider_visible=True)  # dynamic zoom slider
    return fig


def growth_rate_chart(history):
    g = history.copy()
    g["Growth_Rate"] = g["Actual_Cases"].pct_change() * 100
    colors = [COLORS["green"] if x > 0 else COLORS["red"] for x in g["Growth_Rate"].fillna(0)]
    fig = go.Figure(data=[go.Bar(
        x=g["Month"], y=g["Growth_Rate"], marker=dict(color=colors),
        text=[f"{v:.1f}%" if pd.notna(v) else "—" for v in g["Growth_Rate"]],
        textposition="auto",
    )])
    fig.update_layout(**chart_cfg(xlabel="Month", ylabel="Growth Rate (%)"))
    fig.add_hline(y=0, line_dash="dash", line_color="rgba(255,255,255,0.2)")
    return fig


def actual_vs_predicted_chart(df_f):
    """Historical vs Predicted cases per month — from the fact table itself."""
    m = df_f.groupby("year_month")[["historical_cases", "predicted_cases"]].sum().reset_index()
    m = m.sort_values("year_month")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=m["year_month"], y=m["historical_cases"], mode="lines+markers",
        name="Historical Cases", line=dict(color=COLORS["cyan"], width=2.5),
    ))
    fig.add_trace(go.Scatter(
        x=m["year_month"], y=m["predicted_cases"], mode="lines+markers",
        name="Predicted Cases", line=dict(color=COLORS["purple"], width=2.5, dash="dot"),
    ))
    fig.update_layout(**chart_cfg(xlabel="Month", ylabel="Cases"))
    fig.update_xaxes(tickangle=45)
    return fig


def forecast_accuracy_trend_chart(df_f):
    m = df_f.groupby("year_month")["forecast_accuracy_pct"].mean().reset_index()
    m = m.sort_values("year_month")
    fig = go.Figure(go.Scatter(
        x=m["year_month"], y=m["forecast_accuracy_pct"], mode="lines+markers",
        line=dict(color=COLORS["green"], width=2.5),
        marker=dict(size=6), fill="tozeroy", fillcolor="rgba(0,255,135,0.08)",
    ))
    fig.update_layout(**chart_cfg(xlabel="Month", ylabel="Forecast Accuracy (%)"))
    fig.update_xaxes(tickangle=45)
    return fig


def forecast_breakdown_chart(forecast):
    fig = go.Figure(data=[go.Bar(
        x=forecast["Month"], y=forecast["Forecast_Cases"],
        marker=dict(color=forecast["Forecast_Cases"],
                    colorscale=[[0, COLORS["green"]], [0.5, COLORS["gold"]], [1, COLORS["red"]]],
                    showscale=False),
        text=[f"{int(v):,}" for v in forecast["Forecast_Cases"]], textposition="auto",
    )])
    fig.update_layout(**chart_cfg(xlabel="Month", ylabel="Forecasted Cases"))
    fig.update_xaxes(tickangle=45)
    return fig


# ── DECISION ANALYTICS ────
def build_priority_table(df_f) -> pd.DataFrame:
    """
    Outbreak priority per state — a decision score combining:
      predicted vs historical growth (30) + alert level (30)
      + response time (20) + low readiness (20)  → 0-100 score.
    """
    g = df_f.groupby("state_name").agg(
        outbreaks=("outbreak_id", "count"),
        hist_cases=("historical_cases", "sum"),
        pred_cases=("predicted_cases", "sum"),
        max_alert=("alert_level", lambda s: max(s, key=lambda a: ALERT_ORDER.get(a, 0))),
        response=("response_time_hours", "mean"),
        readiness=("hospital_readiness_score", "mean"),
    ).reset_index()

    g["trend_pct"] = ((g["pred_cases"] - g["hist_cases"]) / g["hist_cases"].replace(0, np.nan) * 100).fillna(0)

    alert_w  = g["max_alert"].map(ALERT_ORDER).fillna(0) / 3 * 30
    resp_w   = (g["response"].clip(0, 48) / 48) * 20
    read_w   = ((100 - g["readiness"]).clip(0, 100) / 100) * 20
    trend_w  = g["trend_pct"].clip(0, 100) / 100 * 30
    g["priority_score"] = (alert_w + resp_w + read_w + trend_w).round(1)

    g["priority"] = g["priority_score"].apply(
        lambda s: "🔴 Critical" if s >= 60 else "🟠 High" if s >= 40 else "🟡 Medium" if s >= 20 else "🟢 Low"
    )

    g = g.sort_values("priority_score", ascending=False)
    return g[["state_name", "outbreaks", "max_alert", "trend_pct",
              "response", "readiness", "priority_score", "priority"]]


def display_priority_table(prio: pd.DataFrame):
    view = prio.copy()
    view["trend_pct"] = view["trend_pct"].map(lambda v: f"{v:+.1f}%")
    view["response"] = view["response"].map(lambda v: f"{v:.1f} hrs")
    view["readiness"] = view["readiness"].map(lambda v: f"{v:.1f}%")
    view = view.rename(columns={
        "state_name": "State", "outbreaks": "Outbreaks", "max_alert": "Alert",
        "trend_pct": "Predicted vs Actual", "response": "Avg Response",
        "readiness": "Hospital Readiness", "priority_score": "Priority Score",
        "priority": "Priority",
    })
    st.dataframe(view, width="stretch", hide_index=True)

    top = prio.iloc[0]
    st.markdown(
        f"<div style='background: rgba(255,94,94,0.10); border-left: 4px solid #FF5E5E; "
        f"padding: 12px; border-radius: 6px; margin-top: 10px;'>"
        f"<strong style='color:#FF5E5E;'> Top priority: {top['state_name']}</strong> — "
        f"{top['priority']} (score {top['priority_score']:.0f}/100) · "
        f"{top['outbreaks']} outbreaks, alert {top['max_alert']}, "
        f"predicted vs actual {top['trend_pct']:+.1f}%.</div>",
        unsafe_allow_html=True,
    )


# ── MAIN DASHBOARD ────
def show_outbreak_dashboard():
    load_css()
    df, history, forecast = load_data()

    page_header(
        "Outbreak Monitoring & Forecasting",
        # "Real-time outbreak intelligence · sidebar filters · top state & disease rankings · ARIMA 6-month forecast · decision analytics"
    )
    render_pdf_button("Outbreak_Monitoring_Report")   # top-left: export the report as PDF

    # ── FILTERS (from sidebar bar) ──
    df_f = apply_filters(df)

    # ── KPI ROW 1 — OUTBREAK EVENTS (filtered) ─
    st.markdown("### Outbreak Event KPIs")
    c1, c2, c3, c4 = st.columns(4)
    kpi(c1, "Total Outbreaks", fmt(len(df_f)), accent="gold")
    kpi(c2, f"New Outbreaks · {latest_month_label(df_f)}", fmt(new_outbreak_count(df_f)), accent="cyan")
    kpi(c3, "Emergency Alerts", fmt(int(df_f["emergency_alert_flag"].sum())), accent="red")
    kpi(c4, "Controlled Outbreaks", fmt(int(df_f["controlled_flag"].sum())), accent="green")

    # ── KPI ROW 2 — QUALITY METRICS (filtered) ─
    st.markdown("###  Quality & Readiness KPIs")
    c1, c2, c3, c4, c5 = st.columns(5)
    kpi(c1, "Containment Rate", fmt_pct(df_f["containment_rate_pct"].mean(), 1), accent="green")
    kpi(c2, "Avg Response Time", f"{df_f['response_time_hours'].mean():.1f} hrs", accent="cyan")
    kpi(c3, "Hospital Readiness", fmt_pct(df_f["hospital_readiness_score"].mean(), 1), accent="purple")
    kpi(c4, "Resource Readiness", fmt_pct(df_f["resource_readiness_score"].mean(), 1), accent="gold")
    kpi(c5, "Forecast Accuracy", fmt_pct(df_f["forecast_accuracy_pct"].mean(), 1), accent="red")

    st.divider()

    # ── TABBED LAYOUT: MONITORING | FORECASTING | DECISION ANALYTICS 
    tab_mon, tab_fcst, tab_dec = st.tabs([
        " Monitoring",
        " Forecasting",
        " Decision Analytics",
    ])

    # ── TAB 1 — MONITORING 
    with tab_mon:
        st.markdown("###  What is happening right now?")
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            chart_title("Outbreak Trend Events per Month")
            st.plotly_chart(monthly_trend_chart(df_f), width="stretch")
        with col_m2:
            chart_title("Alert Level Distribution")
            st.plotly_chart(alert_level_chart(df_f), width="stretch")

        col_m3, col_m4 = st.columns(2)
        with col_m3:
            chart_title("Outbreak Severity Funnel")
            st.plotly_chart(severity_funnel(df_f), width="stretch")
        with col_m4:
            chart_title("Response Time Distribution")
            st.plotly_chart(response_time_chart(df_f), width="stretch")

        st.markdown("###  Top 10 by Total Cases")
        col_race1, col_race2 = st.columns(2)
        with col_race1:
            chart_title("Top 10 States by Total Cases")
            st.plotly_chart(top_groups_chart(df_f, "state_name"), width="stretch")
        with col_race2:
            chart_title("Top 10 Diseases by Total Cases")
            st.plotly_chart(top_groups_chart(df_f, "disease_name"), width="stretch")

    # ── TAB 2 — FORECASTING 
    with tab_fcst:
        st.markdown("###  What might happen next?")

        total_cases = int(history["Actual_Cases"].sum())
        peak_cases = int(history["Actual_Cases"].max())
        current_month = int(history["Actual_Cases"].iloc[-1])
        forecast_total = int(forecast["Forecast_Cases"].sum())

        c1, c2, c3, c4 = st.columns(4)
        kpi(c1, "Total Cases (36 mo)", fmt(total_cases), accent="gold",
            delta=f"{(history['Actual_Cases'].tail(3).mean() / history['Actual_Cases'].iloc[-6:-3].mean() - 1) * 100:+.1f}% trend")
        kpi(c2, "Peak Month", fmt(peak_cases), accent="red")
        kpi(c3, "Latest Month", fmt(current_month), accent="cyan")
        kpi(c4, "6-Mo Forecast", fmt(forecast_total), accent="purple",
            delta=f"{(forecast['Forecast_Cases'].iloc[-1] / forecast['Forecast_Cases'].iloc[0] - 1) * 100:+.1f}% outlook")

        col_f1, col_f2 = st.columns([3, 2])
        with col_f1:
            chart_title("Historical + ARIMA Forecast (National)")
            st.plotly_chart(historical_forecast_chart(history, forecast), width="stretch")
        with col_f2:
            chart_title("Monthly Growth Rate")
            st.plotly_chart(growth_rate_chart(history), width="stretch")

        col_f3, col_f4 = st.columns(2)
        with col_f3:
            chart_title("Actual vs Predicted Cases")
            st.plotly_chart(actual_vs_predicted_chart(df_f), width="stretch")
        with col_f4:
            chart_title("Forecast Accuracy by Month")
            st.plotly_chart(forecast_accuracy_trend_chart(df_f), width="stretch")

        col_f5, col_f6 = st.columns([2, 1])
        with col_f5:
            chart_title("6-Month Forecast Breakdown")
            st.plotly_chart(forecast_breakdown_chart(forecast), width="stretch")
        with col_f6:
            st.markdown("### Forecast Metrics")
            st.markdown(f"""
            <div style="display: flex; flex-direction: column; gap: 12px;">
                <div style="background: rgba(255,215,0,0.1); border-left: 4px solid #FFD700; padding: 12px; border-radius: 6px;">
                    <div style="font-size: 12px; color: #94A3B8; margin-bottom: 4px;">HIGHEST FORECAST</div>
                    <div style="font-size: 18px; font-weight: 700; color: #FFD700;">{int(forecast['Forecast_Cases'].max()):,}</div>
                </div>
                <div style="background: rgba(0,255,135,0.1); border-left: 4px solid #00FF87; padding: 12px; border-radius: 6px;">
                    <div style="font-size: 12px; color: #94A3B8; margin-bottom: 4px;">LOWEST FORECAST</div>
                    <div style="font-size: 18px; font-weight: 700; color: #00FF87;">{int(forecast['Forecast_Cases'].min()):,}</div>
                </div>
                <div style="background: rgba(0,229,255,0.1); border-left: 4px solid #00E5FF; padding: 12px; border-radius: 6px;">
                    <div style="font-size: 12px; color: #94A3B8; margin-bottom: 4px;">6-MONTH AVERAGE</div>
                    <div style="font-size: 18px; font-weight: 700; color: #00E5FF;">{int(forecast['Forecast_Cases'].mean()):,}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── TAB 3 — DECISION ANALYTICS ──
    with tab_dec:
        st.markdown("###  Outbreak Priority by State")
        # st.caption("Priority score (0–100) = predicted-vs-actual growth (30) + alert level (30) "
        #            "+ response time (20) + low hospital readiness (20). Sorted by highest priority.")
        prio = build_priority_table(df_f)
        display_priority_table(prio)

    st.divider()

    # # ── KEY INSIGHTS ─
    # st.markdown("###  Key Insights & Recommendations")
    # col_insight1, col_insight2 = st.columns(2)

    # recent_3m = history["Actual_Cases"].tail(3).mean()
    # earlier_3m = history["Actual_Cases"].iloc[-6:-3].mean()
    # trend = ((recent_3m - earlier_3m) / earlier_3m * 100) if earlier_3m > 0 else 0

    # with col_insight1:
    #     if trend > 5:
    #         insight("Recent outbreak cases show an <strong>upward trend</strong>. Immediate action required to monitor hotspots and enhance surveillance.",
    #                 kind="red", title=" Rising Trend Alert")
    #     elif trend < -5:
    #         insight("Outbreak cases are <strong>declining</strong>. Continue preventive measures and maintain current containment protocols.",
    #                 kind="green", title="✅ Positive Trajectory")
    #     else:
    #         insight("Outbreak cases remain <strong>stable</strong>. Maintain current surveillance and response strategies.",
    #                 kind="cyan", title=" Stable Situation")

    # with col_insight2:
    #     fcst_avg = forecast["Forecast_Cases"].mean()
    #     hist_avg = history["Actual_Cases"].mean()
    #     fv = ((fcst_avg - hist_avg) / hist_avg * 100)
    #     if fv > 10:
    #         insight(f"Forecast predicts <strong>higher cases (+{fv:.1f}%)</strong> in the next 6 months. Prepare resources and increase alert levels.",
    #                 kind="red", title="🔴 Forecast Warning")
    #     elif fv < -10:
    #         insight(f"Forecast suggests <strong>improvement (-{abs(fv):.1f}%)</strong> over the next 6 months. Maintain control measures.",
    #                 kind="green", title="🟢 Positive Outlook")
    #     else:
    #         insight(f"Forecast indicates <strong>similar levels</strong> as recent history. Monitor for any sudden changes.",
    #                 kind="cyan", title="📈 Stable Forecast")

    # st.divider()

    # # ── MODEL DETAILS 
    # with st.expander("📊 Model Details & Performance Metrics"):
    #     st.markdown("""
    #     #### ARIMA Forecasting Model
    #     **Model Specification:** ARIMA(1,1,1)
    #     - **AR(1):** Autoregressive component captures last period's cases
    #     - **I(1):** First differencing ensures stationarity
    #     - **MA(1):** Moving average smooths random shocks

    #     **Data pipeline (own module):**
    #     - Raw source: `data/fact_outbreak.csv` → `cleaning/cleaning_pipeline_outbreak.py`
    #     - Cleaned records: `cleaning/fact_outbreak_clean.csv` (2,500 events, 36 months)
    #     - Forecast inputs: `data/dim_date.csv` + `data/monthly_outbreak_history.csv`
    #     - Outputs: `data/outbreak_forecast.csv` (6 months)
    #     - Fact-table forecast fields: `predicted_cases` (per event), `forecast_accuracy_pct` (per event)

    #     **Usage:** Refresh model monthly with latest data via `python outbreak_forecasting.py`.
    #     """)

    # st.markdown("---")
    # st.markdown("""
    # <div style="text-align: center; font-size: 11px; color: #475569; margin-top: 20px;">
    #     🚨 <strong>Outbreak Monitoring & Forecasting</strong> |
    #     Last Updated: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """ |
    #     ARIMA Model v1.0 · Sidebar Filters + Top Rankings + Decision Analytics
    # </div>
    # """, unsafe_allow_html=True)


# ── ENTRY POINT ─
if __name__ == "__main__":
    show_outbreak_dashboard()
