import os
import concurrent.futures
from groq import Groq

def generate_single_editorial(client, category, articles):
    titles = [article.get('title', '') for article in articles if article.get('title')]
    titles_text = "\n- ".join(titles[:15]) # Limit to 15 per category to save tokens
    
    prompt = f"""
Eres un redactor experto especializado en {category}. Tienes los siguientes titulares de hoy sobre esta temática:

- {titles_text}

Redacta un único párrafo breve (máximo 3 frases) en español, resumiendo los temas principales. No hagas listas, solo el párrafo fluido.
"""
    print(f"Empezando a generar resumen IA para: {category}...")
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": f"Eres un periodista experto en {category}."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=350,
        )
        print(f"✅ Resumen generado con éxito para: {category}")
        return category, completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ Error generating editorial for {category}: {e}")
        return category, ""

def generate_category_editorials(articles):
    """
    Generate daily editorials for each category using Groq API.
    """
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("Warning: GROQ_API_KEY not found. Skipping editorial generation.")
        return {}
        
    client = Groq(api_key=api_key, max_retries=1)
    
    # Agrupar articulos por categoria
    articles_by_cat = {}
    for article in articles:
        cat = article.get('category', 'General')
        if cat not in articles_by_cat:
            articles_by_cat[cat] = []
        articles_by_cat[cat].append(article)
        
    editorials = {}
    
    # Generar en paralelo (limitado a 2 para no saturar la API gratuita)
    print(f"Enviando {len(articles_by_cat)} peticiones a Groq...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        futures = []
        for cat, cat_articles in articles_by_cat.items():
            if cat_articles:
                futures.append(executor.submit(generate_single_editorial, client, cat, cat_articles))
                
        for future in concurrent.futures.as_completed(futures):
            cat, text = future.result()
            if text:
                editorials[cat] = text
                
    return editorials
