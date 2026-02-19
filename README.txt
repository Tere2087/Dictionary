# DictionaryPY

Aplicación de escritorio en Python para construir un glosario de inglés de forma rápida: permite buscar palabras (scraping), guardar definiciones y organizar el vocabulario, con exportación a CSV/PDF.

## Motivación
Proyecto personal creado por necesidad real: facilitar la elaboración de un glosario final para una asignatura de inglés, automatizando la obtención de definiciones y el guardado/organización del vocabulario.

## Funcionalidades
- Búsqueda de palabras y obtención de definición mediante scraping (Cambridge Dictionary).
- Guardado de palabras/definiciones en base de datos local (SQLite).
- Organización por carpetas (crear/editar/eliminar) y asignación de palabras a carpetas.
- Exportación a CSV y PDF (por carpeta y/o global).
- Pronunciación en inglés mediante TTS (gTTS).

## Tecnologías
- Python
- Tkinter + ttkbootstrap (GUI)
- requests + BeautifulSoup (scraping)
- SQLite (persistencia)
- fpdf (exportación PDF)
- gTTS + playsound (pronunciación)

## Cómo ejecutar
1. Clona el repositorio
2. Instala dependencias:
   ```bash
   pip install -r requirements.txt
