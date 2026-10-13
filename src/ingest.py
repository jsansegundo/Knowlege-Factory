from pypdf import PdfReader

pdf_path = "data/incentives.pdf"

reader = PdfReader(pdf_path)

text = ""

for page in reader.pages:
    page_text = page.extract_text()

    if page_text:
        text += page_text + "\n"

chunks = []

chunk_size = 1000

for i in range(0, len(text), chunk_size):
    chunk = text[i:i + chunk_size]
    chunks.append(chunk)

print(f"Texto total: {len(text)} caracteres")
print(f"Chunks generados: {len(chunks)}")

print("\nPrimer chunk:\n")
print(chunks[0])
