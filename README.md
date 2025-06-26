# contextAgent

This repository implements an ontology-aware context ingestion pipeline for cybersecurity controls. The project ingests structured knowledge from ontologies and unstructured documents, then enriches that data with entity recognition and reasoning before exporting results for downstream use.

## Components
- **Ontology loader** – reads cybersecurity ontologies using `rdflib` and prepares them for use in the pipeline.
- **Document loader** – processes PDF and text documents with `PyMuPDF` and `pandas`.
- **NER matcher** – identifies concepts in documents using `spacy` and ontology mappings.
- **LangChain agent** – orchestrates ontology lookups, document queries, and reasoning.
- **Output writers** – serialize results to desired formats for analysis or storage.

## Setup
1. Install Python 3.11.
2. Create a virtual environment and install the required libraries:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install rdflib spacy pandas PyMuPDF "langchain>=0.1"
```
