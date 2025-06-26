"""TTL writer using rdflib."""

from __future__ import annotations

from typing import Iterable, Tuple



def write_ttl(triples: Iterable[Tuple[str, str, str]], path: str) -> None:
    """Write ``triples`` to ``path`` in Turtle format."""
    from rdflib import Graph, URIRef  # local import for optional dependency
    graph = Graph()
    for s, p, o in triples:
        graph.add((URIRef(s), URIRef(p), URIRef(o)))
    graph.serialize(destination=path, format="ttl")
