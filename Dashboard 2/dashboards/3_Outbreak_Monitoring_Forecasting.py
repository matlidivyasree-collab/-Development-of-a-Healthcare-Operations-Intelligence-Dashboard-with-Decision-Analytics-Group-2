"""
3_Outbreak_Monitoring_Forecasting.py
---------------------------------------
Empty placeholder for the Outbreak Monitoring & Forecasting dashboard.
Data layer is already wired up via src.data_loader.get_outbreak_master()
for whoever picks this up next.
"""

import streamlit as st

from src.styling import inject_css, page_header

inject_css()
page_header(
    "Outbreak Monitoring & Forecasting",
    "Alert levels, containment performance, and readiness scores",
    badge="EMPTY",
)

st.info("This dashboard is under development. Content coming soon.")
