import feedparser
from datetime import datetime
import time

def fetch_feeds(feed_urls, max_entries=10):
    all_news = []
    
    for url in feed_urls:
        print(f"Descargando RSS: {url}")
        feed = feedparser.parse(url)
        
        feed_title = feed.feed.get('title', 'Desconocido')
        
        for entry in feed.entries[:max_entries]:
            # Intentamos obtener la imagen si existe
            image_url = None
            if 'media_content' in entry and len(entry.media_content) > 0:
                image_url = entry.media_content[0].get('url')
            elif 'links' in entry:
                for link in entry.links:
                    if link.get('type', '').startswith('image/'):
                        image_url = link.get('href')
                        break
            
            # Formatear la fecha
            pub_date = entry.get('published', '')
            if 'published_parsed' in entry and entry.published_parsed:
                dt = datetime.fromtimestamp(time.mktime(entry.published_parsed))
                pub_date = dt.strftime("%d/%m/%Y %H:%M")
                
            all_news.append({
                'source': feed_title,
                'title': entry.get('title', 'Sin título'),
                'link': entry.get('link', '#'),
                'summary': entry.get('summary', ''),
                'date': pub_date,
                'image': image_url
            })
            
    return all_news
