from scraper import scrape_url
from processor_ai import process_text

url = "https://es.wikipedia.org/wiki/Ciencia"

texto = scrape_url(url)
resultado = process_text(texto)

print(resultado)
