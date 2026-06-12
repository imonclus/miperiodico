import os
from rss_reader.fetcher import fetch_feeds
from rss_reader.builder import build_html
from rss_reader.groq_client import generate_editorial

def main():
    print("=== Generador de Periódico RSS ===")
    
    feeds_file = "rss_reader/feeds.txt"
    if not os.path.exists(feeds_file):
        print(f"Error: No se encontró el archivo {feeds_file}.")
        return
        
    with open(feeds_file, "r") as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        
    if not urls:
        print("No hay URLs configuradas en feeds.txt")
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
