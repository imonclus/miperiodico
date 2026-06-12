import os
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from zoneinfo import ZoneInfo

def build_html(articles, editorials_by_category=None, output_file="public/index.html"):
    template_dir = os.path.join(os.path.dirname(__file__), "templates")
    env = Environment(loader=FileSystemLoader(template_dir))
    
    # Create public directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Extract unique categories
    categories = sorted(list(set(article.get('category', 'General') for article in articles)))
    
    template = env.get_template("index.html")
    
    # Extraer las fuentes únicas de los artículos para crear los botones de filtro
    unique_sources = sorted(list(set(article['source'] for article in articles)))
    
    # Render template
    html_content = template.render(
        articles=articles,
        categories=categories,
        sources=unique_sources,
        editorials=editorials_by_category or {},
        last_updated=datetime.now(ZoneInfo("Europe/Madrid")).strftime("%d/%m/%Y %H:%M")
    )
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"\n¡Éxito! Tu periódico digital ha sido generado en: {os.path.abspath(output_file)}")
