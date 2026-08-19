
import streamlit as st
import plotly.graph_objects as go

# ── PROFESSIONAL COLOR PALETTE ──────────────────────────────────────────────
COLORS = {
    "gold": "#FFD700",
    "cyan": "#00E5FF",
    "purple": "#A78BFA",
    "green": "#00FF87",
    "red": "#FF5E5E",
    "orange": "#FB923C",
    "blue": "#38BDF8",
    "pink": "#F472B6",
    "dark_blue": "#0F172A",
    "slate": "#475569",
}

COLOR_SEQUENCE = ["#FFD700", "#00E5FF", "#A78BFA", "#00FF87", "#FF5E5E", "#FB923C", "#38BDF8", "#F472B6"]

# ── THEME COLORS ────────────────────────────────────────────────────────────
THEME = {
    "dark": {
        "bg_base": "#020817",
        "bg_card": "#0d1b2e",
        "bg_sidebar": "#060f1e",
        "text_primary": "#EFF6FF",
        "text_muted": "#94A3B8",
        "text_dim": "#475569",
        "border": "rgba(255,255,255,0.07)",
        "shadow": "0 4px 20px rgba(0,0,0,0.45)",
    }
}

# ── PLOTLY CHART CONFIGURATION ──────────────────────────────────────────────
def chart_cfg(xlabel: str = "", ylabel: str = "") -> dict:
    """
    Returns a professional Plotly layout configuration.
    Chart titles are rendered OUTSIDE the plot (see chart_title()) so they
    never overlap the chart content.
    Args:
        xlabel: X-axis label
        ylabel: Y-axis label
    """
    font_color = "#EFF6FF"
    grid_color = "rgba(255,255,255,0.05)"
    label_color = "#94A3B8"
    hover_bg = "#0d1b2e"
    hover_border = "#FFD700"

    # Configure axes
    xax = dict(
        gridcolor=grid_color,
        zeroline=False,
        showline=False,
        tickfont=dict(color=font_color, size=11),
    )
    yax = dict(
        gridcolor=grid_color,
        zeroline=False,
        showline=False,
        tickfont=dict(color=font_color, size=11),
    )

    if xlabel:
        xax["title"] = dict(text=xlabel, font=dict(color=font_color, size=12), standoff=10)
    if ylabel:
        yax["title"] = dict(text=ylabel, font=dict(color=font_color, size=12), standoff=10)

    layout = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=font_color, family="Rajdhani, Inter, sans-serif", size=12),
        xaxis=xax,
        yaxis=yax,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.28,
            xanchor="center",
            x=0.5,
            font=dict(color=label_color, size=11),
        ),
        margin=dict(l=55, r=20, t=12, b=88),
        colorway=COLOR_SEQUENCE,
        hoverlabel=dict(
            bgcolor=hover_bg,
            font_size=12,
            font_family="Rajdhani, sans-serif",
            bordercolor=hover_border,
        ),
    )

    return layout


def styled(fig):
    """Apply standard styling to a Plotly figure."""
    fig.update_layout(**chart_cfg())
    return fig


def load_css():
    """Load professional CSS styling."""
    with open("style.css", encoding="utf-8") as f:
        base = f.read()
    st.markdown(f"<style>{base}</style>", unsafe_allow_html=True)



# ── PAGE HEADER ─────────────────────────────────────────────────────────────
def page_header(title: str, subtitle: str = ""):
    """Display a professional page header."""
    st.markdown(f"""
    <div class="page-header">
      <div class="ph-title">{title}</div>
      {"<div class='ph-sub'>" + subtitle + "</div>" if subtitle else ""}
    </div>""", unsafe_allow_html=True)


# ── CHART TITLE ─────────────────────────────────────────────────────────────
def chart_title(label: str, icon: str = ""):
    """Display a chart title above the chart box."""
    icon_html = f"<span style='font-size: 16px; margin-right: 8px;'>{icon}</span>" if icon else ""
    st.markdown(
        f'<div class="chart-title">{icon_html}{label}</div>',
        unsafe_allow_html=True
    )


# ── KPI / METRIC BOX ────────────────────────────────────────────────────────
def kpi(col, label: str, value: str, accent: str = "gold", delta: str = ""):
    """
    Display a professional KPI metric box.
    Args:
        col: Streamlit column object
        label: KPI label/name
        value: Main metric value
        accent: Color accent ("gold", "green", "red", "cyan", etc.)
        delta: Change indicator (e.g., "+5.2%" or "-3.1%")
    """
    delta_html = f'<div class="metric-delta">{delta}</div>' if delta else ""
    
    accent_classes = {
        "gold": "mv-gold",
        "green": "mv-green",
        "red": "mv-red",
        "cyan": "mv-cyan",
        "purple": "mv-purple",
    }
    
    accent_class = accent_classes.get(accent, "mv-gold")

    with col:
        st.markdown(f"""
        <div class="metric-box">
          <div class="metric-label">{label}</div>
          <div class="metric-value {accent_class}">{value}</div>
          {delta_html}
        </div>""", unsafe_allow_html=True)


# ── INSIGHT BOX ─────────────────────────────────────────────────────────────
def insight(text: str, kind: str = "gold", title: str = "Key Insight"):
    """
    Display an insight box with a specific kind/color.
    Args:
        text: Insight content (can include HTML)
        kind: "gold", "cyan", "red", "green", "purple"
        title: Insight title
    """
    kind_class = "" if kind == "gold" else kind
    st.markdown(f"""
    <div class="insight-box {kind_class}">
      <div class="insight-title">{title}</div>
      <div class="insight-text">{text}</div>
    </div>""", unsafe_allow_html=True)


# ── NUMBER FORMATTING ──────────────────────────────────────────────────────
def fmt(n: float, prefix: str = "") -> str:
    """
    Format a number in Indian numbering system.
    Args:
        n: Number to format
        prefix: Prefix (e.g., "₹", "$")
    Returns:
        Formatted string (e.g., "₹12.34 Cr", "45.6 K")
    """
    if abs(n) >= 1e7:
        return f"{prefix}{n/1e7:.2f} Cr"
    if abs(n) >= 1e5:
        return f"{prefix}{n/1e5:.1f} L"
    if abs(n) >= 1e3:
        return f"{prefix}{n/1e3:.1f} K"
    return f"{prefix}{n:.0f}"


# ── PERCENTAGE FORMATTING ──────────────────────────────────────────────────
def fmt_pct(n: float, decimals: int = 1) -> str:
    """Format a percentage with specified decimals."""
    return f"{n:.{decimals}f}%"


# ── STAT ROW ────────────────────────────────────────────────────────────────
def stat_row(data: dict, accent_colors: dict = None):
    """
    Display a row of statistics with custom colors.
    Args:
        data: Dict of {"label": "value"}
        accent_colors: Dict of {"label": "color_accent"}
    """
    if accent_colors is None:
        accent_colors = {}

    cols = st.columns(len(data))
    for idx, (col, (label, value)) in enumerate(zip(cols, data.items())):
        accent = accent_colors.get(label, "gold")
        kpi(col, label, value, accent=accent)


# ── PROGRESS BAR ────────────────────────────────────────────────────────────
def progress_bar(label: str, value: float, target: float = 100, color: str = "gold"):
    """Display a professional progress bar."""
    pct = (value / target * 100) if target > 0 else 0
    
    color_map = {
        "gold": "#FFD700",
        "cyan": "#00E5FF",
        "green": "#00FF87",
        "red": "#FF5E5E",
        "purple": "#A78BFA",
    }
    
    bar_color = color_map.get(color, "#FFD700")
    
    st.markdown(f"""
    <div style="margin-bottom: 16px;">
      <div style="font-size: 12px; color: #94A3B8; margin-bottom: 6px; font-weight: 600;">
        {label}: <span style="color: {bar_color}; font-weight: 700;">{pct:.1f}%</span>
      </div>
      <div style="width: 100%; height: 8px; background-color: rgba(255,255,255,0.1); border-radius: 4px; overflow: hidden;">
        <div style="width: {min(pct, 100)}%; height: 100%; background: linear-gradient(90deg, {bar_color}, rgba(255,255,255,0.3)); transition: width 0.3s ease;"></div>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ── BADGE ──────────────────────────────────────────────────────────────────
def badge(text: str, kind: str = "gold"):
    """Display a small badge with custom styling."""
    color_map = {
        "gold": "#FFD700",
        "cyan": "#00E5FF",
        "green": "#00FF87",
        "red": "#FF5E5E",
        "purple": "#A78BFA",
    }
    badge_color = color_map.get(kind, "#FFD700")
    
    return f"""<span style="
        display: inline-block;
        padding: 4px 10px;
        background-color: rgba(255,255,255,0.05);
        border: 1px solid {badge_color};
        color: {badge_color};
        border-radius: 4px;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.5px;
    ">{text}</span>"""


# ── DIVIDER ────────────────────────────────────────────────────────────────
def divider(margin: str = "20px 0"):
    """Display a styled divider."""
    st.markdown(f"""
    <div style="
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,215,0,0.3), transparent);
        margin: {margin};
    "></div>
    """, unsafe_allow_html=True)
