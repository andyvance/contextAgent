"""Ontology label vector lookup using spaCy."""

from __future__ import annotations

import argparse
from typing import Iterable, List, Tuple

import numpy as np
import spacy
from rdflib import Graph, RDFS


class OntologyVectorLookup:
    """Load ontology labels and enable semantic search."""

    def __init__(self, path: str):
        self.graph = Graph()
        self.graph.parse(path, format="ttl")
        self.labels: List[str] = []
        self.uris: List[str] = []
        for subject, _, label in self.graph.triples((None, RDFS.label, None)):
            self.labels.append(str(label))
            self.uris.append(str(subject))
        self.nlp = spacy.load("en_core_web_lg")
        # Precompute label vectors for efficiency using nlp.pipe
        docs = list(self.nlp.pipe(self.labels))
        self.label_vectors = np.stack([doc.vector for doc in docs]) if docs else np.empty((0, 0))
        self.label_norms = np.linalg.norm(self.label_vectors, axis=1) if docs else np.empty(0)

    def search(self, query: str, top_n: int = 3) -> List[Tuple[str, str, float]]:
        """Return top ``top_n`` labels most similar to ``query``."""
        if not self.labels:
            return []
        q_vec = self.nlp(query).vector
        q_norm = np.linalg.norm(q_vec)
        if q_norm == 0:
            return []
        sims = self.label_vectors @ q_vec / (self.label_norms * q_norm + 1e-8)
        idxs = np.argsort(-sims)[:top_n]
        return [
            (self.labels[i], self.uris[i], float(sims[i]))
            for i in idxs
        ]


_lookup: OntologyVectorLookup | None = None


def init_lookup(path: str) -> None:
    """Initialize global lookup instance from ``path``."""
    global _lookup
    _lookup = OntologyVectorLookup(path)


def search_ontology(query: str, top_n: int = 3) -> List[Tuple[str, str, float]]:
    """Search initialized ontology for ``query`` and return matches."""
    if _lookup is None:
        raise RuntimeError("OntologyVectorLookup is not initialized")
    return _lookup.search(query, top_n)


def _cli(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Ontology semantic search")
    parser.add_argument("ontology", help="Path to ontology TTL file")
    parser.add_argument("query", help="Search query")
    parser.add_argument("-n", "--top-n", type=int, default=3)
    args = parser.parse_args(list(argv) if argv is not None else None)

    init_lookup(args.ontology)
    for label, uri, score in search_ontology(args.query, args.top_n):
        print(f"{label}\t{uri}\t{score:.3f}")
    return 0


if __name__ == "__main__":  # pragma: no cover - manual usage
    raise SystemExit(_cli())
