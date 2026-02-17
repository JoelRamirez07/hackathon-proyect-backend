from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
import json

from scraper import scrape_url
from processor_ai import process_text, chat_with_context
from vector_db import add_document, get_collection, search_similar


app = FastAPI(title="Backend Hackathon - Sistema RAG")


# =========================
# MODELOS
# =========================

class ChatRequest(BaseModel):
    pregunta: str
    top_k: int = 3


# =========================
# INGESTA
# =========================

@app.post("/ingestar")
def ingestar_url(url: str):
    try:
        # 1️⃣ Scraping
        texto_crudo = scrape_url(url)

        if not texto_crudo or len(texto_crudo) < 100:
            raise HTTPException(status_code=400, detail="Texto insuficiente")

        # 2️⃣ Procesamiento IA (clasificación + resumen)
        resultado_raw = process_text(texto_crudo)

        # 3️⃣ Limpiar markdown ```json si existe
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
""".strip()

        # 5️⃣ Guardar en ChromaDB
        doc_id = str(uuid.uuid4())

        add_document(
            doc_id=doc_id,
            content=texto_para_embedding,
            metadata={
                "url": url,
                "categoria": resultado["categoria"],
                "palabras_clave": resultado["palabras_clave"]
            }
        )

        return {
            "status": "ok",
            "doc_id": doc_id,
            "categoria": resultado["categoria"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# DEBUG BASE VECTORIAL
# =========================

@app.get("/debug")
def debug_db():
    col = get_collection()
    data = col.get()

    return {
        "total_documentos": len(data["ids"]),
        "ids": data["ids"],
        "metadatas": data["metadatas"]
    }


# =========================
# BÚSQUEDA SEMÁNTICA
# =========================

@app.get("/buscar")
def buscar(query: str, top_k: int = 3):
    try:
        results = search_similar(query, top_k)

        respuesta = []

        if results["documents"] and results["documents"][0]:
            for i in range(len(results["documents"][0])):
                respuesta.append({
                    "distancia": results["distances"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "contenido_preview": results["documents"][0][i][:500]
                })

        return {
            "query": query,
            "total_resultados": len(respuesta),
            "resultados": respuesta
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# CHAT RAG COMPLETO
# =========================

@app.post("/chat")
def chat_rag(data: ChatRequest):
    try:
        # 1️⃣ Buscar contexto relevante
        results = search_similar(data.pregunta, data.top_k)
        documentos = results.get("documents", [[]])[0]

        if not documentos:
            return {
                "pregunta": data.pregunta,
                "respuesta": "No se encontró información suficiente en la base de datos."
            }

        # 2️⃣ Construir contexto
        contexto = "\n\n---\n\n".join(documentos)

        # 3️⃣ Llamar a función especializada de chat
        respuesta = chat_with_context(contexto, data.pregunta)

        return {
            "pregunta": data.pregunta,
            "respuesta": respuesta
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
