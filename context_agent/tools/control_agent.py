"""Process control data and run a LangChain agent."""

from __future__ import annotations

import argparse
from typing import Iterable, List, Optional

from ..loaders.document_loader import load_document
from ..loaders.ontology_loader import load_ontologies
from ..processors.spacy_processor import tokenize_texts
from ..processors.ner_matcher import match_entities
from ..processors.langchain_agent import run_agent, DummyLLM


_DEFAULT_LLM = DummyLLM()


def process_controls(
    docs: Iterable[str] | None = None,
    ontology_files: Iterable[str] | None = None,
    output_ttl: str | None = None,
    llm: Optional[DummyLLM] = None,
) -> List[List[str]]:
    """Load data from ``docs`` and generate TTL using an LLM."""
    llm = llm or _DEFAULT_LLM
    texts: List[str] = []
    if docs:
        for path in docs:
            texts.extend(load_document(path))

    tokens = tokenize_texts(texts)

    ontology = load_ontologies(ontology_files) if ontology_files else {}
    annotations = match_entities(texts, ontology) if ontology else []

    if output_ttl and ontology_files:
        ttl_chunks: List[str] = []
        for text in texts:
            prompt = (
                f"DATA:\n{text}\nANNOTATIONS:{annotations}\n\n"
                f"Use the ontology and annotations to create TTL triples."
            )
            ttl_chunks.append(run_agent(prompt, llm=llm))
        with open(output_ttl, "w", encoding="utf-8") as f:
            f.write("\n".join(ttl_chunks))

    # Run the agent for side effects (e.g., reasoning) over tokenized content
    for toks in tokens:
        run_agent(" ".join(toks), llm=llm)

    return tokens


def _cli(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Process documents with LangChain")
    parser.add_argument("docs", nargs="+", help="Input documents")
    parser.add_argument("-o", "--ontology", action="append", dest="ontology_files")
    parser.add_argument("-t", "--ttl", dest="output_ttl")
    args = parser.parse_args(list(argv) if argv is not None else None)
    tokens = process_controls(
        docs=args.docs,
        ontology_files=args.ontology_files,
        output_ttl=args.output_ttl,
    )
    for tok_list in tokens:
        print(" ".join(tok_list))
    return 0


if __name__ == "__main__":  # pragma: no cover - manual use
    raise SystemExit(_cli())
