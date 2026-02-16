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
