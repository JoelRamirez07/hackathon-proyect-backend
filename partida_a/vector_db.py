import chromadb
from chromadb.config import Settings
import os
from embeddings import generar_embedding

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "db", "chroma")

# ✅ Cliente GLOBAL
client = chromadb.Client(
    Settings(
        persist_directory=DB_PATH,
        is_persistent=True
    )
)

def get_collection():
    return client.get_or_create_collection(name="documentos")

def add_document(doc_id: str, content: str, metadata: dict):
    col = get_collection()

    embedding = generar_embedding(content)

    col.add(
        ids=[doc_id],
        documents=[content],
        metadatas=[metadata],
        embeddings=[embedding]
    )

    print("📦 Documento insertado:", doc_id)

def search_similar(query: str, top_k: int = 3):
    col = get_collection()

    query_embedding = generar_embedding(query)

    results = col.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    return results
