"""Document loader supporting multiple formats."""

from __future__ import annotations

import json
from pathlib import Path
from typing import List
import xml.etree.ElementTree as ET



def load_document(path: str) -> List[str]:
    """Load a document from ``path`` and return text chunks."""
    ext = Path(path).suffix.lower()
    if ext == ".pdf":
        import fitz  # PyMuPDF
        doc = fitz.open(path)
        return [page.get_text() for page in doc]
    if ext in {".xlsx", ".xls"}:
        import pandas as pd  # optional dependency
        df = pd.read_excel(path, header=None)
        return df.fillna("").astype(str).agg(" ".join, axis=1).tolist()
    if ext == ".json":
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [json.dumps(data)]
    if ext == ".xml":
        tree = ET.parse(path)
        root = tree.getroot()
        text = ET.tostring(root, encoding="unicode")
        return [text]
    if ext == ".ttl":
        with open(path, "r", encoding="utf-8") as f:
            return [f.read()]
    with open(path, "r", encoding="utf-8") as f:
        return [f.read()]
