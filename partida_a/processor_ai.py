import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options={"api_version": "v1"}
)

def process_text(text: str):

    prompt = f"""
    Limpia el siguiente texto.
    Clasifícalo en una de estas categorías:
    - Infraestructura
    - Talento
    - Publicaciones
    - Otro

    Devuelve EXCLUSIVAMENTE un JSON válido con:
    - categoria
    - resumen
    - palabras_clave (lista)

    Texto:
    {text[:4000]}
    """

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt
    )

    return response.text
