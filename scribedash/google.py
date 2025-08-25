from __future__ import annotations

import re
from pathlib import Path
import time
import random
import logging
from typing import List

import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
logger = logging.getLogger("scribedash")


def build_service(credentials_path: Path):
    """Build the Google Sheets service client.

    Keep logs at DEBUG to avoid noisy terminal output during frequent refreshes.
    """
    logger.debug("Building Sheets service …")
    creds = Credentials.from_service_account_file(str(credentials_path), scopes=SCOPES)
    return build("sheets", "v4", credentials=creds, cache_discovery=False)


def extract_spreadsheet_id(text: str) -> str:
    if not text:
        return ""
    m = re.search(r"/d/([a-zA-Z0-9-_]+)", text)
    if m:
        return m.group(1)
    return text.strip()


def _with_retries(fn, *, attempts: int = 5, base_delay: float = 0.5, max_delay: float = 5.0):
    """Execute fn() with simple exponential backoff and jitter.

    Logs only on warning level when retries happen to avoid spam.
    """
    last_err = None
    for i in range(attempts):
        try:
            return fn()
        except Exception as e:  # noqa: BLE001 - broad to catch transient transport errors
            last_err = e
            # Jittered exponential backoff
            delay = min(max_delay, base_delay * (2 ** i)) * (0.7 + 0.6 * random.random())
            logger.warning("Transient error on Sheets API call (attempt %s/%s): %s", i + 1, attempts, e)
            time.sleep(delay)
    # After exhausting retries, re-raise
    if last_err is not None:
        raise last_err
    raise RuntimeError("Unknown error in _with_retries without captured exception")


def list_sheet_titles(service, spreadsheet_id: str) -> List[str]:
    def _call():
        return (
            service.spreadsheets()
            .get(spreadsheetId=spreadsheet_id, fields="sheets(properties(title))")
            .execute()
        )

    meta = _with_retries(_call)
    return [s["properties"]["title"] for s in meta.get("sheets", [])]


def fetch_values(service, spreadsheet_id: str, sheet_title: str):
    """Fetch raw values from a sheet with retries and quiet logging."""

    def _call():
        return (
            service.spreadsheets()
            .values()
            .get(
                spreadsheetId=spreadsheet_id,
                range=sheet_title,
                valueRenderOption="FORMATTED_VALUE",
                dateTimeRenderOption="FORMATTED_STRING",
            )
            .execute()
        )

    result = _with_retries(_call)
    return result.get("values", [])


def values_to_dataframe(values):
    if not values:
        return pd.DataFrame()
    max_len = max(len(r) for r in values)
    rows = [r + [""] * (max_len - len(r)) for r in values]
    headers = rows[0]
    has_headers = any(h != "" for h in headers) and len(set(headers)) == len(headers)
    if has_headers:
        return pd.DataFrame(rows[1:], columns=headers)
    return pd.DataFrame(rows)
