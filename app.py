from __future__ import annotations

from datetime import datetime, timezone
import logging
import sys
from pathlib import Path

import streamlit as st
from streamlit_autorefresh import st_autorefresh

from scribedash.config import load_settings
from scribedash.google import build_service, list_sheet_titles, fetch_values, values_to_dataframe


def main():
    st.set_page_config(page_title="ScribeDash", layout="wide")
    st.title("ScribeDash")
    st.caption("Live view + pages. Use the sidebar to control refresh.")

    # Configure logging for terminal visibility
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True,
    )
    log = logging.getLogger("scribedash")

    settings = load_settings(Path(__file__).resolve().parent)
    creds_path = settings.credentials_path
    if not creds_path.exists():
        st.error(f"credentials.json not found at {creds_path}")
        st.stop()

    with st.sidebar:
        st.subheader("Settings")
        if settings.spreadsheet_id:
            st.info("Using Spreadsheet ID from .env")
            spreadsheet_input = settings.spreadsheet_id
        else:
            spreadsheet_input = st.text_input(
                "Spreadsheet ID or URL",
                placeholder="Paste the Google Sheet URL or its ID",
                help="You can paste the full URL (we'll extract the ID) or just the spreadsheet ID.",
            )
        refresh_secs = st.number_input(
            "Refresh interval (seconds)", min_value=2, max_value=60, value=settings.refresh_secs, step=1
        )
        live = st.toggle("Live refresh", value=True)
        st.page_link("pages/1_Executive_Overview.py", label="Executive Overview", icon="📊")

    # Auto-refresh while live mode is on
    if live:
        st_autorefresh(interval=refresh_secs * 1000, key="auto-refresh")

    from scribedash.google import extract_spreadsheet_id
    spreadsheet_id = extract_spreadsheet_id(spreadsheet_input)
    if not spreadsheet_id:
        st.info("Enter a Spreadsheet ID or paste its URL to begin.")
        st.stop()

    try:
        @st.cache_resource(show_spinner=False)
        def service_cached(p: Path):
            logging.getLogger("scribedash").debug("Building Sheets service …")
            return build_service(p)

        service = service_cached(creds_path)

        # Sheet selection (titles cached to reduce API calls and log noise)
        @st.cache_data(ttl=300, show_spinner=False)
        def titles_cached(creds_str: str, sid: str):
            log.debug("Fetching sheet list for spreadsheet %s", sid)
            return list_sheet_titles(service_cached(Path(creds_str)), sid)

        sheet_titles = titles_cached(str(creds_path), spreadsheet_id)
        default_sheet = sheet_titles[0]

        # Maintain selection across refreshes and spreadsheet changes
        sel_key = f"sheet_select_{spreadsheet_id}"
        if sel_key not in st.session_state:
            st.session_state[sel_key] = default_sheet
        selected_sheet = st.sidebar.selectbox(
            "Sheet",
            options=sheet_titles,
            index=sheet_titles.index(st.session_state[sel_key]) if st.session_state[sel_key] in sheet_titles else 0,
        )
        st.session_state[sel_key] = selected_sheet

        # Throttle repetitive fetch logs: only log INFO when sheet changes
        last_sheet_key = "last_logged_sheet"
        last_sheet = st.session_state.get(last_sheet_key)
        if last_sheet != selected_sheet:
            log.info("Reading values from sheet '%s'", selected_sheet)
            st.session_state[last_sheet_key] = selected_sheet
        else:
            log.debug("Reading values from sheet '%s'", selected_sheet)
        values = fetch_values(service, spreadsheet_id, selected_sheet)
        df = values_to_dataframe(values)

        st.subheader(f"Sheet: {selected_sheet}")
        st.caption(
            f"Last fetched: {datetime.now(timezone.utc).astimezone().strftime('%Y-%m-%d %H:%M:%S %Z')}"
        )
        if df.empty:
            st.warning("No data found in the sheet.")
        else:
            log.debug("Fetched %s rows x %s columns", len(df.index), len(df.columns))
            st.dataframe(df, use_container_width=True)
    except Exception as e:
        log.exception("Error while fetching sheet data: %s", e)
        st.error(f"Error: {e}")
        st.stop()


if __name__ == "__main__":
    main()
