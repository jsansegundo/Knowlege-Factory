# Knowledge Factory

Motor documental multiformato basado en Azure AI Foundry.

## Arquitectura

```text
Documents -> Registry -> Loaders -> Document Model -> Chunker -> Embeddings -> FAISS -> Knowledge Chat
```

## Formatos soportados

- PDF
- DOCX
- PPTX

## Componentes

### Registry

- `src/registry.py`: gestiona el registro y los estados de los documentos.
- `src/build_registry.py`: detecta documentos nuevos, existentes y actualizados.

### Loaders

- `src/loaders/pdf_loader.py`
- `src/loaders/docx_loader.py`
- `src/loaders/pptx_loader.py`
- `src/loaders/loader_factory.py`

### Indexación

- `src/index_documents_v2.py`: genera o sustituye los chunks de los documentos pendientes.
- `src/build_knowledge_index.py`: genera embeddings, reconstruye FAISS y activa los documentos.

### Chat

- `src/knowledge_chat.py`: recuperación multilingüe, reranking y respuestas con fuentes.

## Flujo incremental

Coloca los documentos en `documents/` y ejecuta:

```bash
python src/build_registry.py
python src/index_documents_v2.py
python src/build_knowledge_index.py
python src/knowledge_chat.py
```

### 1. Actualizar el Registry

`build_registry.py` calcula la huella de cada documento y detecta documentos nuevos, existentes o actualizados. Los documentos nuevos o modificados quedan como `pending_index`.

### 2. Generar los chunks

`index_documents_v2.py` sustituye los chunks de los documentos pendientes, conserva los demás y actualiza los manifiestos locales.

### 3. Construir el índice

`build_knowledge_index.py` genera los embeddings, reconstruye el índice FAISS y cambia los documentos procesados a `active`.

### 4. Consultar la Knowledge Base

`knowledge_chat.py` aplica búsqueda multilingüe y reranking. Escribe `salir` para cerrar el chat.


## Archivos generados localmente

No se versionan en Git:

- `manifests/all_chunks.json`
- `manifests/manifest.json`
- `manifests/registry.json`
- `documents/`
- `indexes/`
- `logs/`

Si los manifiestos no existen, el flujo los crea durante la ejecución.

## Modelos Azure

- GPT-5 Mini
- `text-embedding-3-small`
