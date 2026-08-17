"""Pytest path setup for Person A package."""

from __future__ import annotations

import sys
from pathlib import Path

DATA_ROOT = Path(__file__).resolve().parents[1]
if str(DATA_ROOT) not in sys.path:
    sys.path.insert(0, str(DATA_ROOT))
