from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class DocumentRetriever:
    """Retrieve the most relevant document chunks for a query."""

    def __init__(self, chunks: list[str]):
        if not chunks:
            raise ValueError("At least one chunk is required.")

        self.chunks = chunks

        self.vectorizer = TfidfVectorizer(
            stop_words="english"
        )

        self.chunk_vectors = self.vectorizer.fit_transform(chunks)

    def search(
        self,
        query: str,
        top_k: int = 3
    ) -> list[tuple[str, float]]:
        """
        Return the most relevant chunks and similarity scores.

        Args:
            query: User's question.
            top_k: Number of chunks to return.

        Returns:
            List of (chunk, similarity_score).
        """

        if not query.strip():
            return []

        query_vector = self.vectorizer.transform([query])

        similarities = cosine_similarity(
            query_vector,
            self.chunk_vectors
        )[0]

        ranked_indices = similarities.argsort()[::-1][:top_k]

        return [
            (self.chunks[index], float(similarities[index]))
            for index in ranked_indices
        ]