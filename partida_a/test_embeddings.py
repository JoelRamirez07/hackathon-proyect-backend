from embeddings import generate_embedding

texto = "La ciencia es un sistema de conocimiento organizado."
vector = generate_embedding(texto)

print("Dimensión del vector:", len(vector))
print(vector[:10])
