import os
from rss_reader.fetcher import fetch_feeds
from rss_reader.builder import build_html

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
    
    # Construir HTML
    output_filename = "public/index.html"
    build_html(all_news, output_file=output_filename)

if __name__ == "__main__":
    main()
