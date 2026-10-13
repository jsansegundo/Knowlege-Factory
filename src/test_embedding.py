from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

client = OpenAI(
    base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY")
)

response = client.embeddings.create(
    model=os.getenv("AZURE_EMBEDDING_DEPLOYMENT"),
    input="Microsoft Defender XDR"
)

vector = response.data[0].embedding

print(f"Dimensiones del vector: {len(vector)}")
print(f"Primeros valores: {vector[:10]}")
