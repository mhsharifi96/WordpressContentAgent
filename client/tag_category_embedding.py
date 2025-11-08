
from langchain_openai import OpenAIEmbeddings
import numpy as np
from numpy.linalg import norm
from domain.wordpress import CategoryData, TagData

class EmbeddingHandler:
    def __init__(self, base_url: str, embeddings: OpenAIEmbeddings):
        self.base_url = base_url
        self.embeddings = embeddings

    async def get_embeddings(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for a batch of texts using LangChain."""
        # LangChain's embedding interface supports batch input
        return await self.embeddings.aembed_documents(texts)

    async def check_category_exists_vector(
        self,
        new_category: str,
        categories: list[CategoryData] | None = None,
        threshold: float = 0.6
    ) -> CategoryData | None:
        """
        Check if a semantically similar category exists using LangChain embeddings.

        Args:
            new_category (str): The category name to check.
            categories (list[CategoryData]): The list of existing categories.
            threshold (float): Cosine similarity threshold (0–1). Default 0.6.

        Returns:
            CategoryData | None: The existing category if semantically similar,
                          otherwise None.
        """
        if not categories:
            return None

        # Prepare list of texts: new category first + all existing names
        names = [new_category] + [c.name for c in categories]

        # Get all embeddings in one async call
        embeddings = await self.get_embeddings(names)

        new_vector = np.array(embeddings[0])
        existing_vectors = [np.array(v) for v in embeddings[1:]]

        # Compute cosine similarities
        similarities = [
            np.dot(new_vector, ev) / (norm(new_vector) * norm(ev))
            for ev in existing_vectors
        ]

        # Find best match
        best_idx = int(np.argmax(similarities))
        best_similarity = similarities[best_idx]

        if best_similarity >= threshold:
            best_match = categories[best_idx]
            print(f"Found similar category: {best_match.name} (similarity={best_similarity:.2f})")
            return best_match

        print(f"No similar category found (max similarity={best_similarity:.2f})")
        return None

    async def check_tag_exists_vector(
        self,
        new_tag: str,
        tags: list[TagData] | None = None,
        threshold: float = 0.6
    ) -> TagData | None:
        """
        Check if a semantically similar tag exists using LangChain embeddings.

        Args:
            new_tag (str): The tag name to check.
            tags (list[tagData]): The list of existing tags.
            threshold (float): Cosine similarity threshold (0–1). Default 0.6.

        Returns:
            tagData | None: The existing tag if semantically similar,
                          otherwise None.
        """
        if not tags:
            return None

        # Prepare list of texts: new tag first + all existing names
        names = [new_tag] + [t.name for t in tags]

        # Get all embeddings in one async call
        embeddings = await self.get_embeddings(names)

        new_vector = np.array(embeddings[0])
        existing_vectors = [np.array(v) for v in embeddings[1:]]

        # Compute cosine similarities
        similarities = [
            np.dot(new_vector, ev) / (norm(new_vector) * norm(ev))
            for ev in existing_vectors
        ]

        # Find best match
        best_idx = int(np.argmax(similarities))
        best_similarity = similarities[best_idx]

        if best_similarity >= threshold:
            best_match = tags[best_idx]
            print(f"Found similar tag: {best_match.name} (similarity={best_similarity:.2f})")
            return best_match

        print(f"No similar tag found (max similarity={best_similarity:.2f})")
        return None