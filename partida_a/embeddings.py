from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def generar_embedding(texto: str):
    vector = model.encode(texto)
    return vector.tolist()
