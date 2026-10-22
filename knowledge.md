# Knowledge Factory

Multi-format document ingestion, indexing, and RAG chat engine built on Python, FAISS, and Azure AI Foundry (Azure OpenAI).

## Overview & Key Code

```text
documents/ -> build_registry.py -> index_documents_v2.py -> build_knowledge_index.py -> knowledge_chat.py
```

- **Registry & Classification**
  - `src/registry.py`: Manages `manifests/registry.json`, SHA-256 document hashing, lifecycle statuses (`new`, `existing`, `updated` -> `pending_index` -> `active`), and controlled corpus metadata validation (`source_authority`, `program`, `document_role`, `canonical_status`).
  - `src/classify_corpus.py`: Catalog (`CORPUS_METADATA`) that assigns controlled metadata to known Microsoft/SEIDOR security workshop and program documents without mutating their technical indexing status.
  - `src/build_registry.py`: Scans `documents/`, updates the registry for `.pdf`, `.docx`, and `.pptx` files, applies corpus classification, and persists `manifests/registry.json` once.
- **Loaders & Models**
  - `src/models/document.py`, `src/models/chunk.py`: `Document` and `Chunk` dataclasses.
  - `src/loaders/`: Format-specific text extractors (`pdf_loader.py`, `docx_loader.py`, `pptx_loader.py`) dispatched through `loader_factory.py` (`extract_text`).
  - `src/chunker.py`: Splits `Document.content` into fixed-size character chunks (default `1000` chars).
- **Indexing & Embeddings**
  - `src/index_documents_v2.py`: Processes `pending_index` documents from the registry, preserves chunks for unchanged documents, computes deterministic `chunk_id` values (`sha256(file_path + "\0" + content):occurrence`), and writes `manifests/all_chunks.json` and `manifests/manifest.json`. Leaves registry status as `pending_index` until embeddings are built.
  - `src/build_knowledge_index.py`: Loads `manifests/all_chunks.json`, reuses cached vectors from `indexes/knowledge_embeddings.npz` (keyed by `chunk_id` and `AZURE_EMBEDDING_DEPLOYMENT`), generates missing embeddings via Azure OpenAI, writes the FAISS `IndexFlatL2` index to `indexes/knowledge.index`, and marks pending documents as `active` in `manifests/registry.json`.
- **Retrieval & Chat**
  - `src/knowledge_chat.py`: Interactive CLI chat (`salir` / `exit` / `quit` to exit). Rewrites user queries to English for bilingual semantic search across FAISS, deduplicates top candidates, runs LLM reranking (up to 4 chunks), and answers strictly from retrieved context with source citations.
- **Tests**
  - `tests/`: Unit tests (`unittest`) covering registry lifecycle, hashing, metadata validation, corpus classification, and incremental embedding caching.
  - `src/test_*.py`: Standalone smoke scripts for loaders, chunking, and embeddings (require sample files in `data/` or live Azure credentials).

## Commands

Run all commands from the **project root** (paths like `documents/`, `manifests/`, and `indexes/` are resolved relative to the current working directory, and imports assume `src` is on `PYTHONPATH` or executed as `python src/<script>.py`).

### Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Required environment variables in `.env`:
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_DEPLOYMENT` (chat/responses model, e.g., GPT-5 Mini)
- `AZURE_EMBEDDING_DEPLOYMENT` (embedding model, e.g., `text-embedding-3-small`)

### Incremental Indexing & Chat Pipeline
```bash
python src/build_registry.py
python src/index_documents_v2.py
python src/build_knowledge_index.py
python src/knowledge_chat.py
```

### Corpus Classification Only
```bash
python src/classify_corpus.py
```

### Tests
Run the `unittest` suite with `PYTHONPATH=src`:
```bash
PYTHONPATH=src .venv/bin/python -m unittest discover -s tests
```

## Conventions, Constraints & Gotchas

- **Working Directory & `PYTHONPATH`**: Scripts use relative paths (`documents/`, `manifests/registry.json`, `manifests/all_chunks.json`, `indexes/knowledge.index`) and top-level imports (`import registry`, `from loaders.loader_factory import ...`). Always run scripts from the repository root and set `PYTHONPATH=src` when invoking `unittest` or modules from outside `src/`.
- **Supported Extensions in Ingestion vs. Catalog**: `build_registry.py`, `index_documents_v2.py`, and `loader_factory.py` only ingest `.pdf`, `.docx`, and `.pptx`. Note that `classify_corpus.py` also contains catalog entries for `.xlsx` files (workbooks/templates) so they can be classified if present in the registry, even though `.xlsx` is ignored by the text ingestion loaders.
- **Separation of Technical State and Metadata**: Applying metadata (`set_document_metadata` / `apply_catalog_to_registry`) must never alter a document's technical lifecycle fields (`status`, `indexed_at`). Likewise, `index_documents_v2.py` does not mark documents `active`; only `build_knowledge_index.py` transitions `pending_index` -> `active` after FAISS and the embedding cache are written.
- **Embedding Cache Integrity**: `indexes/knowledge_embeddings.npz` stores `chunk_ids`, `embeddings`, and `deployment`. If `AZURE_EMBEDDING_DEPLOYMENT` changes, the cache is invalidated and regenerated automatically. Every chunk in `all_chunks.json` must have a non-empty, unique `chunk_id` and non-empty `content`.
- **Generated Local Artifacts**: `documents/`, `manifests/`, `indexes/`, and `logs/` are runtime artifacts and gitignored. Tests should use `tempfile.TemporaryDirectory` or mocks rather than mutating `manifests/registry.json`.
- **Legacy / Backup Scripts**: `src/` contains earlier iterations (`index_documents.py`, `ingest.py`, `generate_embeddings.py`, `chat.py`, `ask.py`, and `*.backup.py`). The active v2 pipeline is `build_registry.py` -> `index_documents_v2.py` -> `build_knowledge_index.py` -> `knowledge_chat.py`.
- **Language**: User-facing CLI output, prompts, and comments are primarily in Spanish; code identifiers and metadata keys/values are in English.
