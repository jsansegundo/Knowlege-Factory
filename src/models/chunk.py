from dataclasses import dataclass


@dataclass
class Chunk:

    document_name: str
    document_type: str

    chunk_number: int

    content: str
