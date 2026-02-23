# 📖 Dictionary – Desktop App in Python

Aplicación de escritorio desarrollada en Python para la creación y gestión de un glosario de inglés de forma automatizada.  
Permite buscar palabras mediante scraping, almacenar definiciones en base de datos local y organizar el vocabulario por carpetas, con exportación a CSV y PDF.

---

## 💡 Motivación

Proyecto personal desarrollado a partir de una necesidad real: automatizar la creación de un glosario final para una asignatura de inglés, evitando búsquedas manuales repetitivas y mejorando la organización del vocabulario.

---

## 🧰 Funcionalidades

- 🔎 Búsqueda automática de definiciones mediante scraping (Cambridge Dictionary)
- 💾 Almacenamiento persistente en base de datos SQLite
- 📁 Organización por carpetas (crear, editar, eliminar)
- 📊 Exportación a CSV y PDF (global o por carpeta)
- 🔊 Pronunciación en inglés mediante Text-to-Speech (gTTS)
- ✏️ Edición y eliminación de palabras guardadas

---

## 🧠 Arquitectura y aspectos técnicos

- Separación entre lógica de scraping, persistencia y GUI
- Uso de SQLite como base de datos local ligera
- Manejo de requests HTTP y parsing HTML con BeautifulSoup
- Gestión de eventos y diseño de interfaz con Tkinter + ttkbootstrap
- Generación dinámica de documentos PDF con fpdf

---

## 👩🏽‍💻 Tecnologías utilizadas

- Python
- Tkinter + ttkbootstrap
- requests
- BeautifulSoup
- SQLite
- fpdf
- gTTS
- playsound

---

## 📸 Capturas de pantalla

<img width="1007" height="763" alt="imagen 1" src="https://github.com/user-attachments/assets/cf385517-a8c8-4abb-a0ca-456a0125a28b" />
<img width="1004" height="786" alt="imagen 2" src="https://github.com/user-attachments/assets/1ed7c3be-b634-4ac6-9185-4eefd994453a" />

---

## 🚀 Posibles mejoras futuras

- Implementación de sistema de autenticación de usuario
- Manejo avanzado de errores de scraping
- Cacheado de consultas para optimización de rendimiento
- Internacionalización multi-idioma
