
from chromadb import PersistentClient
from chromadb.utils import embedding_functions
from app.core.config import settings

class VectorStore:
    def __init__(self, collection_name: str = "rag_collection"):
        # Persistent client (local storage)
        self.client = PersistentClient(path=settings.CHROMA_DB_PATH)

        # Use OpenAI embeddings (or swap with HuggingFace)
        self.embedding_fn = embedding_functions.OpenAIEmbeddingFunction(
            api_key=settings.OPENAI_API_KEY,
            model_name="text-embedding-ada-002"
        )
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_fn
        )

    def add_documents(self, ids, texts, metadatas=None):
        """
        Add docs to Chroma.
        :param ids: List of unique doc IDs
        :param texts: List of text chunks
        :param metadatas: Optional metadata (source, timestamp, etc.)
        """
        self.collection.add(documents=texts, ids=ids, metadatas=metadatas)

    def search(self, query: str, top_k: int = 5):
        """
        Search Chroma with semantic similarity.
        Returns a list of dicts with id, text, metadata.
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k
        )
        docs = []
        for i in range(len(results["ids"][0])):
            docs.append({
                "id": results["ids"][0][i],
                "text": results["documents"][0][i],
                "source": results["metadatas"][0][i].get("source", "unknown")
            })
        return docs

# Dependency for FastAPI
def get_vectorstore():
    return VectorStore()