import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def process_text(text):
    prompt = f"""
    Limpia el siguiente texto.
    Clasifícalo en una de estas categorías:
    - Infraestructura
    - Talento
    - Publicaciones
    - Otro

    Devuelve JSON con:
    - categoria
    - resumen
    - palabras_clave

    Texto:
    {text[:4000]}
    """

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt
    )

    return response.text
def chat_with_context(contexto: str, pregunta: str):
    prompt = f"""
Eres un asistente experto.
Responde únicamente con base en el contexto proporcionado.
No clasifiques el texto.
No devuelvas JSON.
No inventes información.

Si la respuesta no está en el contexto, responde exactamente:
"No se encontró información suficiente en la base de datos."

CONTEXTO:
{contexto}

PREGUNTA:
{pregunta}

RESPUESTA:
"""

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt
    )

    return response.text.strip()