"""Entity matcher using spaCy and ontology labels."""

from __future__ import annotations

from typing import Dict, Iterable, List, Tuple

import spacy

_nlp = spacy.blank("en")


def match_entities(texts: Iterable[str], ontology: Dict[str, str]) -> List[Tuple[str, str]]:
    """Match ontology labels appearing in ``texts``.

    Returns a list of ``(label, uri)`` tuples.
    """
    matches: List[Tuple[str, str]] = []
    for text in texts:
        _nlp(text)  # tokenization side effect
        lower_text = text.lower()
        for label, uri in ontology.items():
            if label in lower_text:
                matches.append((label, uri))
    return matches
