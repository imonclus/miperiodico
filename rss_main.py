import os
import csv
from rss_reader.fetcher import fetch_feeds
from rss_reader.builder import build_html
from rss_reader.groq_client import generate_editorial

def main():
    print("=== Generador de Periódico RSS ===")
    
    feeds_file = "rss_reader/fuentesrss.csv"
    if not os.path.exists(feeds_file):
        print(f"Error: No se encontró el archivo {feeds_file}.")
        return
        
    urls = []
    with open(feeds_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 2:
                url = row[1].strip()
                if url.startswith("http"):
                    urls.append(url)
        
    if not urls:
        print(f"No hay URLs configuradas en {feeds_file}")
        return
        
    print(f"Leyendo {len(urls)} fuentes de noticias...")
    
    # Recopilar noticias
    all_news = fetch_feeds(urls, max_entries=12)
    print(f"Se descargaron {len(all_news)} noticias en total.")
    
    # Generar Editorial del Día con IA
    print("Generando Editorial del Día con IA (Groq)...")
    editorial = generate_editorial(all_news)
    if editorial:
        print("Editorial generado correctamente.")
    else:
        print("No se pudo generar el editorial.")
    
    # Construir HTML
    output_filename = "public/index.html"
    build_html(all_news, editorial=editorial, output_file=output_filename)

if __name__ == "__main__":
    main()
