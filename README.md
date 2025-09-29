# DictionaryPY 2.0

Aplicación de **diccionario inteligente** en Python (Tkinter) con persistencia en **SQLite**, temas modernos con **ttkbootstrap**, exportación a **CSV/PDF**, síntesis de voz con **gTTS**, scraping con **BeautifulSoup** y soporte de **NLTK/WordNet**.

Este README cubre:
- **Despliegue con Docker (noVNC)** — abre la app en tu navegador (Windows y macOS sin dependencias extra).
- **Ejecución local con Python** (Windows y macOS).



## ✨ Características

- Interfaz **Tkinter** con **ttkbootstrap** (temas).
- Búsqueda/gestión de palabras con **SQLite**.
- Exportación **CSV** y **PDF**.
- **Síntesis de voz** con gTTS (requiere Internet).
- Procesamiento lingüístico con **NLTK** (p. ej., `punkt`, `wordnet`).
- **Scraping** con BeautifulSoup.
- Traducciones con **deep-translator**.



## 📦 Estructura del proyecto (mínima)



.
├─ App.py
├─ config.json
├─ requirements.txt
├─ Dockerfile.novnc
├─ docker-compose.yml
├─ .dockerignore
└─ data/                # se crea en runtime (DB, logs, etc.)

`

> La carpeta `data/` se monta dentro del contenedor y conserva la base de datos (`words.db`) y demás archivos persistentes.

---

## 🚀 Despliegue con Docker (noVNC)

Esta modalidad es **multiplataforma**: al iniciar, la app se abre en el navegador vía una sesión gráfica VNC embebida.

### 1) Requisitos

- **Docker** y **Docker Compose v2**.
- Puerto **5800** libre en tu máquina.

### 2) Construir e iniciar

bash
docker compose build
docker compose up -d
`

### 3) Abrir la aplicación

* Visita **[http://localhost:5800](http://localhost:5800)** en tu navegador.

### 4) Persistencia y archivos

* Todo lo que la app genere (p. ej., `words.db`, logs) queda en **`./data`** en tu proyecto.
* Variables útiles en `docker-compose.yml`:

  * `DISPLAY_WIDTH` y `DISPLAY_HEIGHT` para el tamaño de la ventana virtual.
  * `TZ` para la zona horaria.

### 5) Actualizar / parar

bash
docker compose down
docker compose build --no-cache
docker compose up -d


> 📝 **Nota sobre PDF y fuentes**
> Si tu `App.py`/`config.json` apunta a `C:\\Windows\\Fonts\\arial.ttf`, esa ruta **no existe dentro del contenedor**.
> Ajusta `"font_path"` en `config.json` a una fuente presente en la imagen, por ejemplo:
> `"/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"`
> (De lo contrario, la exportación a PDF podría fallar.)

> 🔊 **Nota sobre audio**
> gTTS necesita Internet. La reproducción directa desde el contenedor a tu equipo **puede no oírse**; si no se escucha, guarda el MP3 y reprodúcelo en el host.

---

## 🧰 Ejecución local (Python)

> Válido para **Windows** y **macOS** (sin Docker). Para evitar conflictos, usa entorno virtual.

### 1) Crear entorno e instalar dependencias

bash
python -m venv .venv

# Activar el entorno
# Windows:
.venv\Scripts\activate
# macOS:
# source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt


### 2) Descargar datos NLTK (una vez)

bash
python -c "import nltk; nltk.download('punkt'); nltk.download('wordnet')"


### 3) Lanzar la app

bash
python App.py


### 4) Configuración de fuentes para PDF (opcional)

* En **Windows**, `C:\Windows\Fonts\arial.ttf` suele funcionar.
* En **macOS**, apunta a una TTF del sistema (p. ej., `"/System/Library/Fonts/Supplemental/Arial.ttf"` o usa una DejaVu instalada).
* También puedes configurar la ruta en `config.json` (ver siguiente sección).

---

## ⚙️ Configuración (`config.json`)

Ejemplo:

json
{
  "db_path": "words.db",
  "font_path": "C:\\\\Windows\\\\Fonts\\\\arial.ttf",
  "temp_audio": "temp_audio.mp3",
  "window_size": "1000x700",
  "theme": "superhero"
}


* **db_path**: archivo SQLite; relativo al directorio de trabajo.
* **font_path**: ruta TTF para exportar PDF (ajústala según tu entorno o contenedor).
* **theme**: tema de `ttkbootstrap` (p. ej., `superhero`, `darkly`, `flatly`, etc.).

> En Docker, ajusta `"font_path"` a `"/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"` para asegurar la exportación a PDF.

---

## 🐛 Solución de problemas

* **No carga en el navegador ([http://localhost:5800](http://localhost:5800)):**

  * Comprueba el estado: `docker ps` y `docker logs -f dictionarypy`.
  * Verifica firewall/antivirus y que el puerto 5800 está libre.
* **Fallo al exportar PDF:**

  * Revisa `font_path` en `config.json` (usa una TTF existente).
* **NLTK pide descargar paquetes:**

  * Ejecuta: `python -c "import nltk; nltk.download('punkt'); nltk.download('wordnet')"`
* **No se escucha el audio:**

  * En contenedor, la salida de audio puede no redirigirse a tu equipo. Exporta el MP3 y reprodúcelo localmente.

---

## 📄 Licencia

Derechos reservados por TeCaHerDev@gmail.com

