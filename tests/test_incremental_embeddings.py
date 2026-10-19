import unittest
import numpy as np

from build_knowledge_index import (
    resolve_embeddings
)


class IncrementalEmbeddingTests(
    unittest.TestCase
):

    def test_reuses_all_cached_embeddings(self):

        chunks = [
            {
                "chunk_id": "chunk-a",
                "content": "Contenido A"
            },
            {
                "chunk_id": "chunk-b",
                "content": "Contenido B"
            }
        ]

        cached_ids = [
            "chunk-a",
            "chunk-b"
        ]

        cached_embeddings = np.asarray(
            [
                [1.0, 0.0],
                [0.0, 1.0]
            ],
            dtype="float32"
        )

        calls = []

        def create_embedding(content):

            calls.append(content)

            return [9.0, 9.0]

        (
            result,
            reused,
            generated
        ) = resolve_embeddings(
            chunks,
            cached_ids,
            cached_embeddings,
            create_embedding
        )

        self.assertEqual(
            reused,
            2
        )

        self.assertEqual(
            generated,
            0
        )

        self.assertEqual(
            calls,
            []
        )

        np.testing.assert_array_equal(
            result,
            cached_embeddings
        )

    def test_generates_only_missing_embedding(self):

        chunks = [
            {
                "chunk_id": "chunk-a",
                "content": "Contenido A"
            },
            {
                "chunk_id": "chunk-c",
                "content": "Contenido C"
            }
        ]

        cached_ids = [
            "chunk-a",
            "chunk-b"
        ]

        cached_embeddings = np.asarray(
            [
                [1.0, 0.0],
                [0.0, 1.0]
            ],
            dtype="float32"
        )

        calls = []

        def create_embedding(content):

            calls.append(content)

            return [3.0, 4.0]

        (
            result,
            reused,
            generated
        ) = resolve_embeddings(
            chunks,
            cached_ids,
            cached_embeddings,
            create_embedding
        )

        self.assertEqual(
            reused,
            1
        )

        self.assertEqual(
            generated,
            1
        )

        self.assertEqual(
            calls,
            ["Contenido C"]
        )

        np.testing.assert_array_equal(
            result,
            np.asarray(
                [
                    [1.0, 0.0],
                    [3.0, 4.0]
                ],
                dtype="float32"
            )
        )

    def test_preserves_current_chunk_order(self):

        chunks = [
            {
                "chunk_id": "chunk-b",
                "content": "Contenido B"
            },
            {
                "chunk_id": "chunk-a",
                "content": "Contenido A"
            }
        ]

        cached_ids = [
            "chunk-a",
            "chunk-b"
        ]

        cached_embeddings = np.asarray(
            [
                [1.0, 0.0],
                [0.0, 1.0]
            ],
            dtype="float32"
        )

        (
            result,
            reused,
            generated
        ) = resolve_embeddings(
            chunks,
            cached_ids,
            cached_embeddings,
            lambda content: [9.0, 9.0]
        )

        self.assertEqual(
            reused,
            2
        )

        self.assertEqual(
            generated,
            0
        )

        np.testing.assert_array_equal(
            result,
            np.asarray(
                [
                    [0.0, 1.0],
                    [1.0, 0.0]
                ],
                dtype="float32"
            )
        )


if __name__ == "__main__":

    unittest.main()