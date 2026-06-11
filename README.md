# 🗞️ Agregador de Noticias RSS

Un agregador de noticias rápido y ligero escrito en Python. Lee canales de noticias (RSS) de tus medios favoritos y genera un periódico digital (archivo HTML estático) limpio, moderno y sin publicidad.

Está preparado para ser automatizado mediante **GitHub Actions** y ser publicado gratuitamente a través de **GitHub Pages**.

## ✨ Características

- 📡 **100% Basado en RSS**: Lectura rápida y ética del contenido público.
- 🎨 **Diseño Moderno y Responsivo**: Cuadrícula tipo tarjetas que se adapta a móviles y PC, e incluye Modo Oscuro automático.
- 🔍 **Filtrado Integrado**: Permite ver todas las noticias o filtrarlas instantáneamente por fuente (periódico).
- 🚀 **Despliegue Automático**: Incluye flujo de trabajo (Workflow) para regenerar y desplegar el sitio cada 6 horas en GitHub.

## 🛠️ Instalación y Uso Local

1. Clona el repositorio e inicializa un entorno virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Instala las dependencias necesarias (`feedparser` y `jinja2`):
   ```bash
   pip install -r requirements.txt
   ```

3. Modifica tus fuentes RSS favoritas en el archivo `rss_reader/feeds.txt`.

4. Ejecuta el generador:
   ```bash
   python rss_main.py
   ```

5. Abre el archivo resultante `public/index.html` en cualquier navegador web.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.
