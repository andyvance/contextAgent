import os
from context_agent.loaders.ontology_loader import load_ontology
from context_agent.loaders.document_loader import load_document

FIXTURES = os.path.join(os.path.dirname(__file__), 'fixtures')


def test_load_ontology():
    path = os.path.join(FIXTURES, 'gistCyber.ttl')
    ontology = load_ontology(path)
    assert 'control' in ontology


def test_load_document_json():
    path = os.path.join(FIXTURES, 'sample.json')
    docs = load_document(path)
    assert isinstance(docs, list) and docs


def test_load_document_xml():
    path = os.path.join(FIXTURES, 'sample.xml')
    docs = load_document(path)
    assert isinstance(docs, list) and docs
