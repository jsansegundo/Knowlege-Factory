from loaders.loader_factory import extract_text

pdf_doc = extract_text(
    "data/incentives.pdf"
)

print(pdf_doc.source_file)
print(pdf_doc.source_type)
print(pdf_doc.content[:300])

print("\n" + "-" * 50 + "\n")

docx_doc = extract_text(
    "data/test.docx"
)

print(docx_doc.source_file)
print(docx_doc.source_type)
print(docx_doc.content[:300])