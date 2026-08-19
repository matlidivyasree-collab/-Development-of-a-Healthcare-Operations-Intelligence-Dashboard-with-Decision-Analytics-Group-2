# ================================================================
# FILTERS
# Shared sidebar filter panel.
# ================================================================
# Every dashboard calls the same panel, so the filters look and
# behave the same on all five pages and no page writes its own
# selectbox code.

import streamlit as st


def filter_options(data):
    """Read the choices for each filter box out of the data.

    Months come back in calendar order, taken from the date table
    rather than sorted alphabetically.
    """

    months = (
        data[["MonthNum", "Month"]]
        .drop_duplicates()
        .sort_values("MonthNum")["Month"]
        .tolist()
    )

    return {
        "State": sorted(data["State"].dropna().unique().tolist()),
        "Year": sorted(data["Year"].dropna().unique().tolist()),
        "Month": months,
        "Program": sorted(data["Program"].dropna().unique().tolist())
    }


def sidebar_filters(data, note=None):
    """Draw the sidebar panel and return the chosen values.

    "All" is offered first in every box and means no filter is
    applied for that box.
    """

    st.sidebar.header("🔎 Global Filters")

    options = filter_options(data)

    selected = {}

    for label, choices in options.items():

        selected[label] = st.sidebar.selectbox(
            label,
            options=["All"] + choices,
            key=f"filter_{label}"
        )

    if note:

        st.sidebar.caption(note)

    return selected


def apply_filters(data, selected):
    """Return only the rows matching every chosen filter."""

    filtered = data.copy()

    for column, value in selected.items():

        if value != "All":

            filtered = filtered[filtered[column] == value]

    return filtered


def population_base(data):
    """One row per state and month.

    Children / Adults / Elderly are recorded once per state per
    month and then repeated on every programme row. Summing the raw
    rows would multiply the population by the number of programmes,
    so the age-group figures are always taken from this
    de-duplicated frame.

    Every other measure, including the immunisation count, does
    vary by programme and is summed from the filtered rows instead.
    """

    return data.drop_duplicates(subset=["State", "Year", "Month"])
