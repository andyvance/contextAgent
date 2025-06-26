import os
import pytest

pytest.importorskip("rdflib")

from context_agent.loaders.ontology_loader import load_ontology, load_ontologies
from context_agent.loaders.document_loader import load_document

FIXTURES = os.path.join(os.path.dirname(__file__), 'fixtures')


def test_load_ontology():
    path = os.path.join(FIXTURES, 'gistCyber.ttl')
    ontology = load_ontology(path)
    assert 'control' in ontology


def test_load_ontologies():
    path = os.path.join(FIXTURES, 'gistCyber.ttl')
    ontology = load_ontologies([path, path])
    assert 'control' in ontology and len(ontology) >= 1


def test_load_document_json():
    path = os.path.join(FIXTURES, 'sample.json')
    docs = load_document(path)
    assert isinstance(docs, list) and docs


def test_load_document_xml():
    path = os.path.join(FIXTURES, 'sample.xml')
    docs = load_document(path)
    assert isinstance(docs, list) and docs

def test_load_document_nist_catalog():
    path = os.path.join(FIXTURES, 'nist_catalog.json')
    docs = load_document(path)
    assert isinstance(docs, list) and docs
