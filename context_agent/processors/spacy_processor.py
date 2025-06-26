"""Utilities for processing text with spaCy."""

from __future__ import annotations

from typing import Iterable, List

import spacy

_nlp = None


def tokenize_texts(texts: Iterable[str]) -> List[List[str]]:
    """Return tokenized versions of ``texts`` using spaCy."""
    global _nlp
    if _nlp is None:
        _nlp = spacy.blank("en")
    docs = _nlp.pipe(texts)
    return [[token.text for token in doc] for doc in docs]
