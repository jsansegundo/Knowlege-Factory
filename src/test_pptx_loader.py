from loaders.loader_factory import extract_text

doc = extract_text(
    "data/test.pptx"
)

print(doc.source_file)
print(doc.source_type)

print("\n")

print(doc.content[:1500])