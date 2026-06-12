import os
from groq import Groq

def generate_editorial(articles):
    """
    Generate a daily editorial using the Groq API based on the fetched articles.
    """
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("Warning: GROQ_API_KEY not found. Skipping editorial generation.")
        return ""
    
    try:
        client = Groq(api_key=api_key)
        
        # Extract titles to create a prompt
        titles = [article.get('title', '') for article in articles if article.get('title')]
        
        # If there are too many, we just take the first 30 to not exceed token limits unnecessarily
        titles_text = "\n- ".join(titles[:30])
        
        prompt = f"""
Eres el redactor jefe de un periódico digital. Tienes los siguientes titulares de las noticias más destacadas de hoy:

- {titles_text}

Tu tarea es escribir "El Editorial del Día". Redacta un único párrafo breve (máximo 4-5 frases) en español, con un tono periodístico, profesional y neutro, resumiendo los temas principales o el ambiente general de las noticias de hoy. No hagas listas, simplemente escribe un párrafo fluido y fácil de leer.
"""

        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "Eres un periodista experto."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=250,
        )
        
        editorial = completion.choices[0].message.content.strip()
        return editorial

    except Exception as e:
        print(f"Error generating editorial with Groq: {e}")
        return ""
