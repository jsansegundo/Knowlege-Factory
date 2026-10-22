import json
import os
from pathlib import Path

import faiss
import numpy as np
from dotenv import load_dotenv
from flask import Flask, abort, render_template_string, request, send_from_directory

from knowledge_chat import enrich_chunks_with_registry_metadata
from knowledge_pipeline import ask_knowledge
from openai_client import create_openai_client
from registry import load_registry

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOWNLOAD_FOLDER = PROJECT_ROOT / "outputs" / "frontier_workshop" / "aenor"


def list_documents():
    if not DOWNLOAD_FOLDER.is_dir():
        return []
    return sorted(p.name for p in DOWNLOAD_FOLDER.glob("*.pptx"))

app = Flask(__name__)

load_dotenv(PROJECT_ROOT / ".env")

client = create_openai_client()
index = faiss.read_index(str(PROJECT_ROOT / "indexes" / "knowledge.index"))

with open(PROJECT_ROOT / "manifests" / "all_chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

enrich_chunks_with_registry_metadata(chunks, load_registry())

PAGE = """
<!doctype html>
<html lang="es">
<head><meta charset="utf-8"><title>Knowledge Chat</title>
<style>
body { font-family: sans-serif; max-width: 800px; margin: 2rem auto; }
textarea { width: 100%; height: 80px; }
pre { white-space: pre-wrap; background: #f4f4f4; padding: 1rem; }
</style></head>
<body>
<h1>Knowledge Chat</h1>
<form method="post" action="/">
  <textarea name="question" placeholder="Escribe tu pregunta">{{ question or "" }}</textarea>
  <br><button type="submit">Preguntar</button>
</form>
{% if answer %}
  <h2>Respuesta</h2>
  <pre>{{ answer }}</pre>
  <h2>Fuentes</h2>
  <ul>{% for source in sources %}<li>{{ source }}</li>{% endfor %}</ul>
{% endif %}
<h2>Documentos del workshop</h2>
<ul>{% for name in documents %}<li><a href="/descargas/{{ name }}">{{ name }}</a></li>{% endfor %}</ul>
</body></html>
"""


def ask(question):
    return ask_knowledge(client, index, chunks, question)


@app.route("/", methods=["GET", "POST"])
def home():
    question = request.form.get("question", "").strip() if request.method == "POST" else ""
    answer = None
    sources = []

    if question:
        answer, sources = ask(question)

    return render_template_string(
        PAGE, question=question, answer=answer, sources=sources, documents=list_documents()
    )


@app.route("/descargas/<path:name>")
def download(name):
    if not name.endswith(".pptx") or not (DOWNLOAD_FOLDER / name).is_file():
        abort(404)
    return send_from_directory(DOWNLOAD_FOLDER, name, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=False, port=5000)
