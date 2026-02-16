import requests
from bs4 import BeautifulSoup

def scrape_url(url: str):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Extraer texto visible
    texts = []

    for tag in soup.find_all(["p", "li"]):
        content = tag.get_text(strip=True)
        if content and len(content) > 40:
            texts.append(content)

    full_text = " ".join(texts)

    return full_text
