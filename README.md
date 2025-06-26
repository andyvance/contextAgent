# contextAgent

This repository implements an ontology-aware context ingestion pipeline for cybersecurity controls. The project ingests structured knowledge from ontologies and unstructured documents, then enriches that data with entity recognition and reasoning before exporting results for downstream use.

## Components
- **Ontology loader** – reads cybersecurity ontologies using `rdflib` and prepares them for use in the pipeline.
- **Document loader** – processes PDF and text documents with `PyMuPDF` and `pandas`.
- **NER matcher** – identifies concepts in documents using `spacy` and ontology mappings.
- **LangChain agent** – orchestrates ontology lookups, document queries, and reasoning.
- **Output writers** – serialize results to desired formats for analysis or storage.
- **Ontology vector lookup** – performs semantic similarity search over ontology labels using spaCy vectors.

## Setup
1. Install Python 3.11.
2. Create a virtual environment and install the required libraries:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install rdflib spacy pandas PyMuPDF "langchain>=0.1"
```

### Running Tests

After installing dependencies, run the unit tests with `pytest`:

```bash
pytest -q
```

### Ontology Vector Lookup Demo

Run a semantic search over an ontology file:

```bash
python -m context_agent.tools.ontology_vector_lookup path/to/ontology.ttl "your query" -n 5
```

### Simple Ingestion Example

Process a set of documents using one or more ontologies and write the results to a TTL file.  The tool extracts text from the provided documents, performs a vector similarity search over the ontology labels, and emits TTL triples linking the best matches.  A similarity threshold can be supplied to tune matching aggressiveness:

```bash
python -m context_agent.tools.process_documents \
    -o path/to/onto1.ttl -o path/to/onto2.ttl \
    -d docs/report.pdf -d controls.xlsx \
    -t 0.7 \
    output.ttl
```

This approach works well for enumerated lists of controls or attack steps
found in spreadsheets or JSON files.  Each row or object in the file is
converted to text and compared with the ontology so that related concepts
are linked in the resulting TTL.

### Control Agent CLI

The `context_agent.tools.control_agent` module exposes a command-line
interface that ingests any number of documents and prints a spaCy token
stream for inspection.  When ontology files and an output path are
provided, TTL triples are also generated.

```bash
python -m context_agent.tools.control_agent \
    path/to/catalog.json controls.xlsx other.pdf \
    -o path/to/ontology.ttl -t output.ttl
```

The command prints the tokenized representation to standard output,
which can help diagnose how the text will be fed into an LLM.
