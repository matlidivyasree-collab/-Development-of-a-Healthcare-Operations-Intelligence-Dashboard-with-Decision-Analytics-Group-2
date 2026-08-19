"""
filters.py
----------
Renders the shared sidebar filter panel (State, Year, Month, Disease Type,
Primary Source, Region) and returns the selections as a dict. Selections are
persisted in st.session_state so they stay in sync as the user moves between
the Executive Overview and Disease Surveillance pages.
"""

import streamlit as st
from src.data_loader import get_filter_options


FILTER_KEYS = [
    "f_region", "f_state", "f_year", "f_month",
    "f_disease_cat", "f_disease", "f_source",
]


def _clear_filters():
    # Runs BEFORE the script reruns and widgets are re-instantiated,
    # so it's safe to write to these session_state keys here.
    for key in FILTER_KEYS:
        st.session_state[key] = []


def render_sidebar_filters() -> dict:
    options = get_filter_options()

    st.sidebar.markdown("## 🔎 Filters")
    st.sidebar.caption("Applies across all visuals on this page")

    region = st.sidebar.multiselect(
        "Region", options["regions"], default=[], key="f_region"
    )
    state = st.sidebar.multiselect(
        "State", options["states"], default=[], key="f_state"
    )
    year = st.sidebar.multiselect(
        "Year", options["years"], default=[], key="f_year"
    )
    month = st.sidebar.multiselect(
        "Month", options["months"], default=[], key="f_month"
    )
    disease_category = st.sidebar.multiselect(
        "Disease Type", options["disease_categories"], default=[], key="f_disease_cat"
    )
    disease = st.sidebar.multiselect(
        "Disease", options["diseases"], default=[], key="f_disease"
    )
    source = st.sidebar.multiselect(
        "Primary Source", options["sources"], default=[], key="f_source"
    )

    st.sidebar.divider()
    st.sidebar.button(
        "♻️ Reset Filters",
        use_container_width=True,
        on_click=_clear_filters,
    )

    st.sidebar.divider()
    st.sidebar.caption("Infosys Public Health Analytics · Internal Use")

    return {
        "regions": region,
        "states": state,
        "years": year,
        "months": month,
        "disease_categories": disease_category,
        "diseases": disease,
        "sources": source,
    }
