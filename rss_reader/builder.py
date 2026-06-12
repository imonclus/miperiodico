import os
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from zoneinfo import ZoneInfo

def build_html(articles, editorial="", output_file="public/index.html"):
    template_dir = os.path.join(os.path.dirname(__file__), "templates")
    env = Environment(loader=FileSystemLoader(template_dir))
    
    template = env.get_template("index.html")
    
    # Extraer las fuentes únicas de los artículos para crear los botones de filtro
    unique_sources = sorted(list(set(article['source'] for article in articles)))
    
    html_content = template.render(
        articles=articles,
        sources=unique_sources,
        editorial=editorial,
        current_time=datetime.now(ZoneInfo("Europe/Madrid")).strftime("%d/%m/%Y %H:%M")
    )
    
    # Crear la carpeta de destino si no existe (importante para github pages)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"\n¡Éxito! Tu periódico digital ha sido generado en: {os.path.abspath(output_file)}")
