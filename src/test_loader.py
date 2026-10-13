from loaders.pdf_loader import extract_text

text = extract_text(
    "data/incentives.pdf"
)

print(text[:1000])