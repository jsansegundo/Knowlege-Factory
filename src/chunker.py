from models.chunk import Chunk


def chunk_document(
    document,
    chunk_size=1000
):

    chunks = []

    text = document.content

    counter = 1

    for i in range(
        0,
        len(text),
        chunk_size
    ):

        chunk_text = text[
            i:i + chunk_size
        ]

        chunks.append(

            Chunk(
                document_name=document.source_file,
                document_type=document.source_type,
                chunk_number=counter,
                content=chunk_text
            )
        )

        counter += 1

    return chunks