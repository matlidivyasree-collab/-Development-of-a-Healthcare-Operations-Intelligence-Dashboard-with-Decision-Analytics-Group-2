# ================================================================
# MEDICAL OPERATIONS INTELLIGENCE
# APPLICATION ENTRY POINT
# ================================================================
# This file sets the page up, applies the theme and builds the
# navigation. Every chart and every calculation lives in the
# dashboards and src folders, so this file stays small.

from pathlib import Path

import streamlit as st

from src.theme import apply_theme


# ================================================================
# PAGE CONFIGURATION
# ================================================================
# set_page_config must be the first Streamlit call in the app.

st.set_page_config(
    page_title="Medical Operations Intelligence",
    page_icon="🩺",
    layout="wide"
)


apply_theme()


# ================================================================
# BUILD THE NAVIGATION
# ================================================================
# Every .py file in the dashboards folder becomes a page. The number
# at the front of the file name sets the order and is removed from
# the label, so 4_Health_Programs_Population_Vulnerability.py is
# shown as "Health Programs Population Vulnerability".
#
# A new dashboard is added by dropping its file into the folder.
# Nothing in this file needs to change.

DASHBOARD_DIR = Path(__file__).parent / "dashboards"


def page_title(file_path):
    """Turn 4_Health_Programs.py into 'Health Programs'."""

    name = file_path.stem

    if "_" in name and name.split("_")[0].isdigit():

        name = name.split("_", 1)[1]

    return name.replace("_", " ")


dashboard_files = sorted(
    f for f in DASHBOARD_DIR.glob("*.py")
    if not f.name.startswith("_")
)


if not dashboard_files:

    st.error(
        "No dashboards were found in the dashboards folder."
    )

    st.stop()


pages = [
    st.Page(
        str(f),
        title=page_title(f),
        icon="🩺"
    )
    for f in dashboard_files
]


# ================================================================
# RUN THE CHOSEN DASHBOARD
# ================================================================

navigation = st.navigation(pages, position="sidebar")

navigation.run()
