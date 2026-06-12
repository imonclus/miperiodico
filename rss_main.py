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
        
    feeds = []
    current_category = "General"
    with open(feeds_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row: continue
            
            # Detectar cabecera de categoría
            if row[0] and (len(row) == 1 or not row[1].strip() or not row[1].startswith("http")) and row[0] != "Medio":
                cat_name = row[0].strip()
                # Limpiar prefijo "1. "
                import re
                cat_name = re.sub(r'^\d+\.\s*', '', cat_name)
                if cat_name and not cat_name.startswith("0"): # Evitar las ultimas lineas raras
                    current_category = cat_name.capitalize() if cat_name.islower() else cat_name
                    
            if len(row) >= 2:
                url = row[1].strip()
                if url.startswith("http"):
                    feeds.append({"url": url, "category": current_category})
        
    if not feeds:
        print(f"No hay URLs configuradas en {feeds_file}")
        return
        
    print(f"Leyendo {len(feeds)} fuentes de noticias...")
    
    # Recopilar noticias
    all_news = fetch_feeds(feeds, max_entries=12)
    print(f"Se descargaron {len(all_news)} noticias en total.")
    
    # Generar Editoriales del Día por Categoría
    from rss_reader.groq_client import generate_category_editorials
    print("Generando Editoriales por Categoría con IA (Groq)...")
    editorials_by_category = generate_category_editorials(all_news)
    
    # Construir HTML
    output_filename = "public/index.html"
    build_html(all_news, editorials_by_category=editorials_by_category, output_file=output_filename)

if __name__ == "__main__":
    main()
