from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Tuple

import pandas as pd

from .google import fetch_values, values_to_dataframe


@dataclass
class SheetResult:
    name: str
    df: pd.DataFrame


def _parse_int_safe(x) -> Optional[int]:
    try:
        return int(x)
    except Exception:
        return None


def _parse_float_safe(x) -> Optional[float]:
    try:
        return float(x)
    except Exception:
        return None


def _parse_date_safe(x) -> Optional[datetime]:
    # Expect dd/mm/yy or ISO-like strings from formatted values
    for fmt in ("%d/%m/%y", "%Y-%m-%d", "%m/%d/%Y"):
        try:
            return datetime.strptime(str(x), fmt)
        except Exception:
            continue
    return None


def load_patient_count(service, spreadsheet_id: str) -> SheetResult:
    values = fetch_values(service, spreadsheet_id, "Patient Count")
    df = values_to_dataframe(values)
    # Normalize column names
    df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
    # Coerce month columns
    for col in [
        "jan",
        "feb",
        "mar",
        "apr",
        "may",
        "jun",
        "july",
        "august",
        "avg",
    ]:
        if col in df.columns:
            df[col] = df[col].apply(_parse_int_safe)
    return SheetResult("Patient Count", df)


def load_utilization(service, spreadsheet_id: str) -> SheetResult:
    values = fetch_values(service, spreadsheet_id, "Utilization")
    df = values_to_dataframe(values)
    df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
    # Attempt numeric coercion for utilization metrics
    for c in df.columns:
        if any(k in c for k in ["january", "february", "march", "april", "may", "june", "july", "august", "average"]):
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return SheetResult("Utilization", df)


def load_dataset(service, spreadsheet_id: str) -> SheetResult:
    values = fetch_values(service, spreadsheet_id, "Dataset")
    df = values_to_dataframe(values)
    df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
    return SheetResult("Dataset", df)


def load_month_activity(service, spreadsheet_id: str, month_title: str) -> SheetResult:
    values = fetch_values(service, spreadsheet_id, month_title)
    df = values_to_dataframe(values)
    # expected columns (Name, Lead, Date, Primary, Task, Provider Covered, Backup Coverage, ...)
    df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
    # Parse some typed columns when present
    for c in ["scheduled", "uploaded"]:
        if c in df.columns:
            df[c] = df[c].apply(_parse_int_safe)
    if "date" in df.columns:
        df["date_parsed"] = df["date"].apply(_parse_date_safe)
    # Hours fields may be numeric strings
    for c in ["scribe_hours", "provider_hours", "hours_difference"]:
        if c in df.columns:
            df[c] = df[c].apply(_parse_float_safe)
    return SheetResult(month_title, df)


def pick_current_month_title(candidates: list[str]) -> Tuple[str, list[str]]:
    # Prefer an exact calendar month name, else first candidate
    month_names = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    for m in month_names[::-1]:  # prefer later in year if multiple
        if m in candidates:
            rest = [c for c in candidates if c != m]
            return m, rest
    return candidates[0], candidates[1:]
