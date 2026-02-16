import json

from scraper import scrape_url
from processor_ai import process_text
from embeddings import generar_embedding


url = "https://es.wikipedia.org/wiki/Ciencia"

# 1️⃣ Scraping
texto_crudo = scrape_url(url)

print("LONGITUD TEXTO:", len(texto_crudo))


# 2️⃣ Limpieza IA
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


# 5️⃣ Construir texto semántico para embedding
palabras = ", ".join(resultado["palabras_clave"])

texto_para_embedding = f"""
Categoría: {resultado['categoria']}

Resumen:
{resultado['resumen']}

Palabras clave:
{palabras}
"""

print("\nTexto para embedding:\n", texto_para_embedding[:500])


# 6️⃣ Generar embedding (local, 384 dimensiones)
vector = generar_embedding(texto_para_embedding)

print("\nDimensión del vector:", len(vector))
print("Primeros 5 valores:", vector[:5])
