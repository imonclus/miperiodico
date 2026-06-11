---
description: Crear una herramienta para analizar información de sitios web con profundidad de análisis configurable.
---

1. Definir especificaciones tecnológicas: Pregunta al usuario qué lenguaje de programación y librerías prefiere (por ejemplo, Python con BeautifulSoup/Scrapy, o Node.js con Cheerio/Puppeteer) y el formato de salida esperado (JSON, CSV, Markdown).

2. Inicializar el proyecto: Crea la estructura de carpetas necesaria y los archivos base, e instala las dependencias seleccionadas por el usuario.

3. Implementar el extractor base (Scraper): Escribe el código principal para leer y extraer la información relevante (texto, metadatos, encabezados) de una única página web (URL).

4. Añadir soporte para profundidad de análisis (Crawling): Implementa la lógica para seguir enlaces internos basándose en un parámetro de profundidad (`depth`). Por ejemplo: `depth=0` solo analiza la página dada, `depth=1` analiza la página dada y las páginas enlazadas desde ella. Asegúrate de implementar un control de URLs visitadas para evitar bucles.

5. Soportar múltiples sitios (Procesamiento por lotes): Extiende la herramienta para que acepte una lista de URLs como entrada (ya sea por línea de comandos o leyendo un archivo), iterando sobre ellas y aplicando el extractor a cada una.

6. Implementar el exportador de resultados: Desarrolla la funcionalidad para estructurar y guardar los datos extraídos en un archivo final.

7. Prueba y validación: Pide al usuario una URL de prueba o utiliza una de demostración, ejecuta la herramienta de análisis y verifica que los resultados recolectados sean correctos.
