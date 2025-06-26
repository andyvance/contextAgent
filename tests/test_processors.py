from context_agent.processors.ner_matcher import match_entities


def test_match_entities():
    ontology = {'control': 'http://example.com/Control'}
    texts = ['This control enforces security.']
    matches = match_entities(texts, ontology)
    assert ('control', 'http://example.com/Control') in matches
