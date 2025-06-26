import os
from context_agent.writers.csv_writer import write_csv
from context_agent.writers.ttl_writer import write_ttl


def test_write_csv(tmp_path):
    out = tmp_path / 'out.csv'
    write_csv([["a", "b"], ["c", "d"]], out)
    assert out.read_text().startswith('a,b')


def test_write_ttl(tmp_path):
    out = tmp_path / 'out.ttl'
    triples = [(
        'http://example.com/s',
        'http://example.com/p',
        'http://example.com/o')]
    write_ttl(triples, out)
    assert out.exists() and out.read_text()
