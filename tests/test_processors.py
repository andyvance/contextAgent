import pytest

pytest.importorskip("spacy")

from context_agent.processors.ner_matcher import match_entities


def test_match_entities():
    ontology = {'control': 'http://example.com/Control'}
    texts = ['This control enforces security.']
    matches = match_entities(texts, ontology)
    assert ('control', 'http://example.com/Control') in matches


def test_vector_match_entities(monkeypatch):
    from context_agent.processors.ner_matcher import vector_match_entities

    class DummyDoc:
        def __init__(self, text: str) -> None:
            self.vector = [1.0] if text.lower() == 'control' else [0.0]

    class DummyNLP:
        def __call__(self, text: str) -> DummyDoc:
            return DummyDoc(text)

        def pipe(self, texts):
            for t in texts:
                yield DummyDoc(t)

    monkeypatch.setattr('spacy.load', lambda _: DummyNLP())
    monkeypatch.setattr('numpy.stack', lambda seq: [d.vector for d in seq])
    monkeypatch.setattr('numpy.linalg.norm', lambda v, axis=None: 1.0)
    monkeypatch.setattr('numpy.argsort', lambda arr: [0])

    ontology = {'control': 'http://example.com/Control'}
    texts = ['control']
    matches = vector_match_entities(texts, ontology, threshold=0.0)
    assert matches
