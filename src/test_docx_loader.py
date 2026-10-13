from loaders.docx_loader import extract_text

text = extract_text(
    "data/test.docx"
)

print(text[:1000])