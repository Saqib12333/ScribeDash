from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import streamlit as st

from scribedash.config import load_settings
from scribedash.google import build_service, list_sheet_titles
from scribedash.ingest import (
    load_dataset,
    load_patient_count,
    load_utilization,
    pick_current_month_title,
    load_month_activity,
)


@st.cache_resource(show_spinner=False)
def get_service(creds_path: Path):
    return build_service(creds_path)


@st.cache_data(ttl=300, show_spinner=False)
def cached_titles(creds_path: str, spreadsheet_id: str):
    return list_sheet_titles(get_service(Path(creds_path)), spreadsheet_id)


def kpi_card(label: str, value, help_text: str | None = None):
    col = st.container(border=True)
    col.metric(label, value)
    if help_text:
        col.caption(help_text)


def page():
    st.set_page_config(page_title="ScribeDash - Executive Overview", layout="wide")
    st.title("Executive Overview")
    st.caption("Key KPIs at a glance. Auto-refresh enabled from the main app settings.")

    settings = load_settings()
    if not settings.spreadsheet_id:
        st.warning("Missing SPREADSHEET_ID in .env. Open the main page to configure.")
        st.stop()

    service = get_service(settings.credentials_path)
    titles = cached_titles(str(settings.credentials_path), settings.spreadsheet_id)
    if not titles:
        st.error("No sheets found.")
        st.stop()

    # Ingest core tabs
    dataset = load_dataset(service, settings.spreadsheet_id).df
    patient = load_patient_count(service, settings.spreadsheet_id).df
    util = load_utilization(service, settings.spreadsheet_id).df
    month_title, _ = pick_current_month_title(titles)
    month_df = load_month_activity(service, settings.spreadsheet_id, month_title).df

    # Compute KPIs aligned with business semantics
    total_scribes = dataset.shape[0] if not dataset.empty else int(month_df.get("name", pd.Series(dtype=str)).nunique())
    active_providers = month_df["provider_covered"].nunique() if "provider_covered" in month_df else 0

    # Patient count (current month) from Patient Count sheet
    month_key = month_title.lower()
    patient_this_month = 0
    if month_key in patient.columns:
        patient_this_month = int(pd.to_numeric(patient[month_key], errors="coerce").sum())

    # Hours and utilization from current month activity
    scribe_hours = float(pd.to_numeric(month_df.get("scribe_hours", pd.Series(dtype=float)), errors="coerce").sum()) if "scribe_hours" in month_df else 0.0
    provider_hours = float(pd.to_numeric(month_df.get("provider_hours", pd.Series(dtype=float)), errors="coerce").sum()) if "provider_hours" in month_df else 0.0
    util_ratio = (scribe_hours / provider_hours) if provider_hours else 0.0

    # Layout KPI cards
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        kpi_card("Total Scribes", total_scribes)
    with c2:
        kpi_card("Active Providers", active_providers)
    with c3:
        kpi_card("Month", month_title)
    with c4:
        kpi_card("Patient Count", f"{patient_this_month:,}")
    with c5:
        kpi_card("Utilization", f"{util_ratio*100:.1f}%", help_text="Scribe hours / Provider hours")

    c6, c7, _ = st.columns(3)
    with c6:
        kpi_card("Scribe Hours", f"{scribe_hours:,.1f}")
    with c7:
        kpi_card("Provider Hours", f"{provider_hours:,.1f}")

    st.divider()
    st.subheader("Trends (preview)")
    if not patient.empty:
        month_cols = [c for c in patient.columns if c in ["jan","feb","mar","apr","may","jun","july","august"]]
        if month_cols:
            long_df = patient.melt(id_vars=[c for c in patient.columns if c not in month_cols], value_vars=month_cols, var_name="month", value_name="count")
            long_df = long_df.dropna(subset=["count"])  # ignore blanks
            if not long_df.empty:
                st.line_chart(long_df.groupby("month")["count"].sum())
    else:
        st.info("Patient Count sheet empty or unavailable.")


if __name__ == "__main__":
    page()
