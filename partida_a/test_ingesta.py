from scraper import scrape_url
from processor_ai import process_text

url = "https://es.wikipedia.org/wiki/Ciencia"

texto = scrape_url(url)

print("LONGITUD TEXTO:", len(texto))
print(texto[:500])  # ver primeros caracteres

resultado = process_text(texto)
print(resultado)
