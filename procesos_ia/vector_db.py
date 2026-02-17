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

    documents = results.get("documents") or []
    metadatas = results.get("metadatas") or []
    distances = results.get("distances") or []

    # Validar estructura
    if not documents or not metadatas or not distances:
        return {"documents": [], "metadatas": [], "distances": []}

    docs = documents[0] if len(documents) > 0 else []
    mets = metadatas[0] if len(metadatas) > 0 else []
    dists = distances[0] if len(distances) > 0 else []

    filtered_docs = []
    filtered_metas = []
    filtered_dists = []

    for doc, meta, dist in zip(docs, mets, dists):
        if dist <= 1.6:
            filtered_docs.append(doc)
            filtered_metas.append(meta)
            filtered_dists.append(dist)

    return {
        "documents": [filtered_docs],
        "metadatas": [filtered_metas],
        "distances": [filtered_dists]
    }