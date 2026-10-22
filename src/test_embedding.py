from pathlib import Path
from math import isfinite
from dotenv import load_dotenv
from openai import OpenAI
import os

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")


def required_env(name):
    value = os.getenv(name)
    if not value:
        raise RuntimeError(
            f"Falta la variable de entorno requerida: {name}"
        )
    return value


endpoint = required_env("AZURE_OPENAI_ENDPOINT").rstrip("/") + "/"
deployment = required_env("AZURE_EMBEDDING_DEPLOYMENT")

client = OpenAI(
    base_url=endpoint,
    api_key=required_env("AZURE_OPENAI_API_KEY"),
)

response = client.embeddings.create(
    model=deployment,
    input="Microsoft Defender XDR",
)

vector = response.data[0].embedding

if not vector:
    raise RuntimeError("Azure OpenAI devolvió un vector vacío.")

finite_count = sum(isfinite(value) for value in vector)

if finite_count!= len(vector):
    raise RuntimeError(
        f"El vector contiene valores no finitos: "
        f"{finite_count}/{len(vector)}"
    )

print(f"Endpoint utilizado: {endpoint}")
print(f"Deployment utilizado: {deployment}")
print(f"Dimensiones del vector: {len(vector)}")
print(f"Valores finitos: {finite_count}")
print(f"Primeros valores: {vector[:10]}")
