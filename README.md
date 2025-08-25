# ScribeDash
## Run

1) Create/activate a virtual env and install requirements
2) Put `credentials.json` (service account) in project root
3) Create a `.env` like:

```
SPREADSHEET_ID=your-google-sheet-id
REFRESH_SECS=5
```

Notes:
- We also accept aliases `Spreadsheet_ID` or `SHEET_ID` for convenience.
- REFRESH_SECS is constrained to 2-60 and used as default; you can override in the UI.

4) Start the app:

```
streamlit run app.py
```

5) Use the sidebar to:
- Toggle live refresh and set interval
- Jump to the Executive Overview page (pages/1_Executive_Overview.py)

```
SPREADSHEET_ID=17SFltoaYiEVVHDN7flctrHn1TKj01xCCyrsoiCN7L8c
# Optional: control auto-refresh interval (2-60 seconds)
REFRESH_SECS=5
```

## Run
```powershell
streamlit run .\app.py
```
Open the browser link shown (e.g., http://localhost:8501), paste your Sheet URL or ID, and keep Live refresh on.

## Features
- Uses service account to read Sheets (read-only scope)
- Auto-refresh polling (configurable interval)
- Select which sheet/tab to view
- INFO-level terminal logs (start, sheet list, fetch, row/col counts)

## Notes
- Real-time: Achieved via periodic polling and page auto-refresh.
- Headers: If the first row looks like headers (unique, non-empty), they’re used; else the raw grid is shown.

## Troubleshooting
- 403/404 errors: Ensure the service account email has been granted access to the Google Sheet.
- Empty data: Confirm data exists on the selected tab and the first row is not entirely blank.
- No logs: The app sets logging to INFO; confirm you’re running via `streamlit run` in the terminal.
