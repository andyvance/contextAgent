"""Simple ontology loader using rdflib."""

from __future__ import annotations

from rdflib import Graph, RDFS
from typing import Dict


def load_ontology(path: str) -> Dict[str, str]:
    """Parse a TTL ontology file and return a label to URI lookup."""
    graph = Graph()
    graph.parse(path, format="ttl")
    lookup: Dict[str, str] = {}
    for subject, _, label in graph.triples((None, RDFS.label, None)):
        lookup[str(label).lower()] = str(subject)
    return lookup
