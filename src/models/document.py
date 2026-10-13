from dataclasses import dataclass


@dataclass
class Document:

    source_file: str

    source_type: str

    content: str