import chromadb
from chromadb.config import Settings
import os
from embeddings import generar_embedding


# Ruta persistente
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "db", "chroma")


def get_client():
    return chromadb.Client(
        Settings(
            persist_directory=DB_PATH,
            is_persistent=True
        )
    )


def get_collection():
    client = get_client()

    return client.get_or_create_collection(
        name="documentos"
    )


def add_document(doc_id: str, text: str, metadata: dict):
    col = get_collection()

    # 🔥 Generamos embedding aquí
    embedding = generar_embedding(text)

    col.add(
        ids=[doc_id],
        documents=[text],
        metadatas=[metadata],
        embeddings=[embedding]
    )
