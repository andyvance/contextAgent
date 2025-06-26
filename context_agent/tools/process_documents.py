"""Simple pipeline for processing documents with an ontology."""

from __future__ import annotations

import argparse
from typing import Iterable

from ..loaders.ontology_loader import load_ontologies
from ..loaders.document_loader import load_document
from ..processors.ner_matcher import vector_match_entities
from ..writers.ttl_writer import write_ttl


def process(
    ontology_paths: Iterable[str],
    docs: Iterable[str],
    out_path: str,
    threshold: float = 0.6,
) -> None:
    """Load ``ontology_paths`` and ``docs`` then write matches to ``out_path``."""
    ontology = load_ontologies(ontology_paths)
    texts: list[str] = []
    for path in docs:
        texts.extend(load_document(path))
    matches = vector_match_entities(texts, ontology, threshold)
    triples = [
        (f"http://example.com/match/{i}", "http://example.com/entity", uri)
        for i, (_, uri) in enumerate(matches)
    ]
    write_ttl(triples, out_path)


def _cli(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Process documents and output TTL")
    parser.add_argument("output", help="Path to output TTL file")
    parser.add_argument(
        "-o",
        "--ontology",
        action="append",
        required=True,
        dest="ontologies",
        help="Ontology TTL file (repeat for multiple)",
    )
    parser.add_argument(
        "-d",
        "--document",
        action="append",
        required=True,
        dest="documents",
        help="Document to process (repeat for multiple)",
    )
    parser.add_argument(
        "-t",
        "--threshold",
        type=float,
        default=0.6,
        help="Similarity threshold for matches",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)
    process(args.ontologies, args.documents, args.output, args.threshold)
    return 0


if __name__ == "__main__":  # pragma: no cover - manual use
    raise SystemExit(_cli())
