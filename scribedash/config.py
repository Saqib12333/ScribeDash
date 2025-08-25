from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    spreadsheet_id: str
    refresh_secs: int = 5
    credentials_path: Path = Path("credentials.json")


def load_settings(root: Optional[Path] = None) -> Settings:
    """Load settings from .env with sensible fallbacks and aliases.

    Aliases supported for spreadsheet id: SPREADSHEET_ID, Spreadsheet_ID, SHEET_ID.
    """
    root = root or Path(__file__).resolve().parents[1]
    env_path = root / ".env"
    if env_path.exists():
        load_dotenv(env_path)

    # Accept a few common aliases and strip quotes
    raw_id = (
        os.getenv("SPREADSHEET_ID")
        or os.getenv("Spreadsheet_ID")
        or os.getenv("SHEET_ID")
        or ""
    ).strip().strip('"').strip("'")

    refresh_raw = (os.getenv("REFRESH_SECS") or "").strip()
    try:
        refresh_secs = int(refresh_raw)
    except ValueError:
        refresh_secs = 5
    refresh_secs = max(2, min(60, refresh_secs))

    creds_path = root / "credentials.json"

    return Settings(spreadsheet_id=raw_id, refresh_secs=refresh_secs, credentials_path=creds_path)
