"""CSV writer using Python's csv module."""

from __future__ import annotations

import csv
from typing import Iterable, Sequence


def write_csv(rows: Iterable[Sequence[str]], path: str) -> None:
    """Write ``rows`` to ``path`` as CSV."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)
