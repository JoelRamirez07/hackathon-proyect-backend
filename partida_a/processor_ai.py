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
