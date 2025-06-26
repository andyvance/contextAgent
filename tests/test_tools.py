import os
import types
import pytest

spacy = pytest.importorskip("spacy")
pytest.importorskip("rdflib")
pytest.importorskip("numpy")

from context_agent.tools.ontology_vector_lookup import OntologyVectorLookup
from langchain.llms.base import LLM

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


from context_agent.tools.control_agent import process_controls


def test_process_controls(monkeypatch, tmp_path):
    # Use dummy spaCy to speed up tests
    class DummyToken:
        def __init__(self, text):
            self.text = text

    class DummyDoc(list):
        def __init__(self, text):
            super().__init__([DummyToken(t) for t in text.split()])

    class DummyNLP:
        def __call__(self, text):
            return DummyDoc(text)

        def pipe(self, texts):
            for t in texts:
                yield DummyDoc(t)

    class DummyLLM(LLM):
        @property
        def _llm_type(self) -> str:
            return "dummy"

        def _call(self, prompt: str, stop: list[str] | None = None) -> str:
            return "@prefix ex: <http://example.com/> . ex:s ex:p ex:o ."

    monkeypatch.setattr("spacy.blank", lambda _: DummyNLP())
    out = tmp_path / "out.ttl"
    tokens = process_controls(
        docs=[os.path.join(FIXTURES, "nist_catalog.json")],
        ontology_files=[os.path.join(FIXTURES, "gistCyber.ttl")],
        output_ttl=str(out),
        llm=DummyLLM(),
    )
    assert tokens
    assert out.exists() and out.read_text()
