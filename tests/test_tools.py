import os
import types
import pytest

spacy = pytest.importorskip("spacy")
pytest.importorskip("rdflib")
pytest.importorskip("numpy")

from context_agent.tools.ontology_vector_lookup import OntologyVectorLookup

FIXTURES = os.path.join(os.path.dirname(__file__), "fixtures")


class DummyDoc:
    def __init__(self, text: str) -> None:
        self.vector = [1.0] if text.lower() == "control" else [0.0]


class DummyNLP:
    def __call__(self, text: str) -> DummyDoc:  # type: ignore[override]
        return DummyDoc(text)

    def pipe(self, texts):
        for t in texts:
            yield DummyDoc(t)


def test_vector_lookup(monkeypatch):
    monkeypatch.setattr("spacy.load", lambda _: DummyNLP())
    path = os.path.join(FIXTURES, "gistCyber.ttl")
    lookup = OntologyVectorLookup(path)
    results = lookup.search("control", top_n=1)
    assert results
    label, uri, score = results[0]
    assert label.lower() == "control"
    assert uri
    assert score >= 0.0

