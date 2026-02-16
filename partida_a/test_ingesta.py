import json
import uuid

from scraper import scrape_url
from processor_ai import process_text
from embeddings import generar_embedding
from vector_db import add_document


# URL de prueba
url = "https://es.wikipedia.org/wiki/Ciencia"


# 1️⃣ Scraping
texto_crudo = scrape_url(url)
print("LONGITUD TEXTO:", len(texto_crudo))


# 2️⃣ Limpieza y clasificación con IA (Gemini)
resultado_raw = process_text(texto_crudo)
print("\nResultado IA RAW:\n", resultado_raw)


# 3️⃣ Limpiar markdown ```json si existe
resultado_raw = (
    resultado_raw
    .replace("```json", "")
    .replace("```", "")
    .strip()
)


# 4️⃣ Convertir a diccionario real
resultado = json.loads(resultado_raw)
print("\nResultado convertido a dict:\n", resultado)


# 5️⃣ Construir texto semántico para embeddings
palabras = ", ".join(resultado["palabras_clave"])

texto_para_embedding = f"""
Categoría: {resultado['categoria']}

Resumen:
{resultado['resumen']}

Palabras clave:
{palabras}
""".strip()

print("\nTexto para embedding (preview):\n", texto_para_embedding[:500])


# 6️⃣ Generar embedding (local, 384 dimensiones)
vector = generar_embedding(texto_para_embedding)

print("\nDimensión del vector:", len(vector))
print("Primeros 5 valores:", vector[:5])


# 7️⃣ Guardar en base de datos vectorial (ChromaDB)
doc_id = str(uuid.uuid4())

add_document(
    doc_id=doc_id,
    text=texto_para_embedding,
    metadata={
        "fuente": url,
        "categoria": resultado["categoria"],
        "palabras_clave": resultado["palabras_clave"]
    }
)

print(f"\n✅ Documento guardado en BD con ID: {doc_id}")
