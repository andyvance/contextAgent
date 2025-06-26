"""Simple ontology loader using rdflib."""

from __future__ import annotations

from typing import Dict, Iterable


def load_ontology(path: str) -> Dict[str, str]:
    """Parse a TTL ontology file and return a label to URI lookup."""
    from rdflib import Graph, RDFS  # local import for optional dependency
    graph = Graph()
    graph.parse(path, format="ttl")
    lookup: Dict[str, str] = {}
    for subject, _, label in graph.triples((None, RDFS.label, None)):
        lookup[str(label).lower()] = str(subject)
    return lookup


def load_ontologies(paths: Iterable[str]) -> Dict[str, str]:
    """Load and merge multiple ontology files into a single lookup."""
    merged: Dict[str, str] = {}
    for path in paths:
        merged.update(load_ontology(path))
    return merged
