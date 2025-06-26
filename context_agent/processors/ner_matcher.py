"""Entity matcher using spaCy and ontology labels."""

from __future__ import annotations

from typing import Dict, Iterable, List, Tuple

_nlp = None


def match_entities(texts: Iterable[str], ontology: Dict[str, str]) -> List[Tuple[str, str]]:
    """Match ontology labels appearing in ``texts``.

    Returns a list of ``(label, uri)`` tuples.
    """
    import spacy  # local import for optional dependency
    global _nlp
    if _nlp is None:
        _nlp = spacy.blank("en")
    matches: List[Tuple[str, str]] = []
    for text in texts:
        _nlp(text)  # tokenization side effect
        lower_text = text.lower()
        for label, uri in ontology.items():
            if label in lower_text:
                matches.append((label, uri))
    return matches


def vector_match_entities(
    texts: Iterable[str],
    ontology: Dict[str, str],
    threshold: float = 0.6,
) -> List[Tuple[str, str]]:
    """Match text to ontology labels using spaCy vectors.

    Returns a list of ``(label, uri)`` tuples whose similarity is above
    ``threshold``.
    """
    import spacy  # optional heavy dependency
    import numpy as np

    nlp = spacy.load("en_core_web_lg")
    labels = list(ontology.keys())
    docs = list(nlp.pipe(labels))
    label_vecs = np.stack([d.vector for d in docs]) if docs else np.empty((0, 0))
    label_norms = np.linalg.norm(label_vecs, axis=1) if docs else np.empty(0)

    matches: List[Tuple[str, str]] = []
    for text in texts:
        q_vec = nlp(text).vector
        q_norm = np.linalg.norm(q_vec)
        if q_norm == 0 or not label_vecs.size:
            continue
        sims = label_vecs @ q_vec / (label_norms * q_norm + 1e-8)
        best = int(np.argmax(sims))
        if sims[best] >= threshold:
            label = labels[best]
            matches.append((label, ontology[label]))
    return matches
