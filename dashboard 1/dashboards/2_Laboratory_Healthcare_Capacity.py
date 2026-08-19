"""
2_Laboratory_Healthcare_Capacity.py
--------------------------------------
Empty placeholder for the Laboratory & Healthcare Capacity dashboard.
Data layer is already wired up via src.data_loader.get_lab_master() for
whoever picks this up next.
"""

import streamlit as st

from src.styling import inject_css, page_header

st.set_page_config(
    page_title="Public Health Analytics | Laboratory & Healthcare Capacity",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()
page_header(
    "Laboratory & Healthcare Capacity",
    "Testing, positivity, vaccination, and hospital capacity",
    badge="EMPTY",
)

st.info("This dashboard is under development. Content coming soon.")
