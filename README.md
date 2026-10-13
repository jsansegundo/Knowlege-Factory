Knowledge Factory
Motor documental multiformato basado en Azure AI Foundry.

Arquitectura
Documents ↓ Loaders ↓ Document Model ↓ Chunker ↓ Embeddings ↓ FAISS ↓ Knowledge Chat

Formatos soportados
PDF
DOCX
PPTX
Componentes
Loaders
pdf_loader.py
docx_loader.py
pptx_loader.py
Chat
knowledge_chat.py
Indexación
index_documents_v2.py
build_knowledge_index.py
Estructura
documents/ indexes/ manifests/ logs/ src/

Modelos Azure
GPT-5 Mini
text-embedding-3-small
