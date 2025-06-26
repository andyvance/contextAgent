import os
import pytest

pytest.importorskip("spacy")
pytest.importorskip("numpy")
pytest.importorskip("rdflib")

from context_agent.tools.process_documents import process

FIXTURES = os.path.join(os.path.dirname(__file__), "fixtures")


def test_process(tmp_path):
    ontology = os.path.join(FIXTURES, "gistCyber.ttl")
    doc = os.path.join(FIXTURES, "sample.json")
    out = tmp_path / "out.ttl"
    process([ontology], [doc], out)
    assert out.exists() and out.read_text()
