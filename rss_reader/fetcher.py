import feedparser
from datetime import datetime
import time
import concurrent.futures
import socket

# Timeout global para evitar bloqueos si una web no responde
socket.setdefaulttimeout(10)

def parse_single_feed(feed_info, max_entries):
    url = feed_info["url"]
    category = feed_info.get("category", "General")
    print(f"Descargando RSS: {url}")
    try:
        feed = feedparser.parse(url)
    except Exception as e:
        print(f"Fallo de conexión al descargar {url}: {e}")
        return []
    
    feed_title = feed.feed.get('title', 'Desconocido')
    parsed_news = []
    
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
            
        parsed_news.append({
            'source': feed_title,
            'category': category,
            'title': entry.get('title', 'Sin título'),
            'link': entry.get('link', '#'),
            'summary': entry.get('summary', ''),
            'date': pub_date,
            'image': image_url
        })
    return parsed_news

def fetch_feeds(feeds, max_entries=10):
    all_news = []
    
    # Usar ThreadPoolExecutor para descargar múltiples RSS en paralelo
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(parse_single_feed, feed_info, max_entries): feed_info for feed_info in feeds}
        for future in concurrent.futures.as_completed(futures):
            try:
                news = future.result()
                all_news.extend(news)
            except Exception as exc:
                url = futures[future]["url"]
                print(f"Error procesando {url}: {exc}")
                
    return all_news
