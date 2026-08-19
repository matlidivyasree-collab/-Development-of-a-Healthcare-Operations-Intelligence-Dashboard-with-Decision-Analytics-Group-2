"""
app.py
------
Single entry point for the Public Health Analytics multipage app.

Wires the 5-dashboard suite into one left-hand navigation menu (via
st.navigation) so the whole suite can be presented from one running app.

Order in the sidebar = order below. Executive Public Health Overview is
first and loads by default; it's the only dashboard that's fully built out
(it contains two tabs internally: Executive Summary and Disease
Surveillance, sharing one filter panel). The other four are empty
placeholders (data layer already wired up in src/data_loader.py) ready to
be filled in as each one is finished.

Run with:  streamlit run app.py
"""

import streamlit as st

st.set_page_config(
    page_title="HealthSentinel",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

executive_overview = st.Page(
    "dashboards/0_Executive_Public_Health_Overview.py",
    title="Executive Public Health Overview",
    default=True,
)
geographic_environmental = st.Page(
    "dashboards/1_Geographic_Environmental_Intelligence.py",
    title="Geographic & Environmental Intelligence",
)
laboratory_healthcare = st.Page(
    "dashboards/2_Laboratory_Healthcare_Capacity.py",
    title="Laboratory & Healthcare Capacity",
)
outbreak_monitoring = st.Page(
    "dashboards/3_Outbreak_Monitoring_Forecasting.py",
    title="Outbreak Monitoring & Forecasting",
)
health_programs_vulnerability = st.Page(
    "dashboards/4_Health_Programs_Population_Vulnerability.py",
    title="Health Programs & Population Vulnerability",
)

# Flat list -> plain left-nav list, no section header, matching the existing
# look. Add further st.Page(...) entries here for any future dashboard.
pg = st.navigation(
    [
        executive_overview,
        geographic_environmental,
        laboratory_healthcare,
        outbreak_monitoring,
        health_programs_vulnerability,
    ]
)

pg.run()
