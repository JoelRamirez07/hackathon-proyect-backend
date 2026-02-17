from fastapi import FastAPI, HTTPException
import uuid
import json

from scraper import scrape_url
from processor_ai import process_text
from vector_db import add_document, get_collection

app = FastAPI(title="Backend Hackathon")


@app.post("/ingestar")
def ingestar_url(url: str):
    try:
        # 1️⃣ Scraping
        texto_crudo = scrape_url(url)

        if not texto_crudo or len(texto_crudo) < 100:
            raise HTTPException(status_code=400, detail="Texto insuficiente")

        # 2️⃣ Procesamiento IA
        resultado_raw = process_text(texto_crudo)

        # 3️⃣ Limpiar markdown ```json
        resultado_raw = (
            resultado_raw
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        resultado = json.loads(resultado_raw)

        # 4️⃣ Construir texto semántico
        palabras = ", ".join(resultado["palabras_clave"])

        texto_para_embedding = f"""
Categoría: {resultado['categoria']}

Resumen:
{resultado['resumen']}

Palabras clave:
{palabras}
"""

        # 5️⃣ Guardar en BD
        doc_id = str(uuid.uuid4())

        add_document(
            doc_id=doc_id,
            content=texto_para_embedding,
            metadata={
                "url": url,
                "categoria": resultado["categoria"]
            }
        )

        return {
            "status": "ok",
            "doc_id": doc_id,
            "categoria": resultado["categoria"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 🔎 ENDPOINT PARA VER LOS INSERTS
@app.get("/debug")
def debug_db():
    col = get_collection()
    data = col.get()

    return {
        "total_documentos": len(data["ids"]),
        "ids": data["ids"],
        "metadatas": data["metadatas"]
    }

@app.get("/buscar")
def buscar(query: str, top_k: int = 3):
    try:
        from vector_db import search_similar

        results = search_similar(query, top_k)

        respuesta = []

        if results["documents"] and results["documents"][0]:
            for i in range(len(results["documents"][0])):
                respuesta.append({
                    "distancia": results["distances"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "contenido": results["documents"][0][i][:500]
                })

        return {
            "query": query,
            "total": len(respuesta),
            "resultados": respuesta
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
