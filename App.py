# Importación de librerías necesarias
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import ttkbootstrap as tb  # Tema moderno para Tkinter
from ttkbootstrap.constants import *  # Constantes para estilos
import sqlite3  # Base de datos SQLite
import os
import csv  # Exportación a CSV
from gtts import gTTS  # Google Text-to-Speech
from playsound import playsound  # Reproducción de audio
import requests  # Para realizar scraping
from bs4 import BeautifulSoup  # Para analizar HTML
import nltk  # Procesamiento de lenguaje natural
from nltk.corpus import wordnet  # Base de datos de palabras en inglés
from fpdf import FPDF  # Exportación a PDF
from deep_translator import GoogleTranslator  # Para traducir

# Descargar datos necesarios de NLTK
nltk.download('wordnet')

class SmartDictionaryApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Diccionario Inteligente 📘 - por TeCaHerDev 😊")
        self.master.geometry("1000x700")

        self.db_path = "words.db"
        self.words = {}
        self.current_word = ""

        self.create_database()
        self.create_menu()
        self.create_widgets()
        self.load_words()

    def create_database(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
                  CREATE TABLE IF NOT EXISTS palabras (
                                                          palabra TEXT PRIMARY KEY,
                                                          definicion TEXT,
                                                          sinonimos TEXT
                  )
                  ''')
        c.execute('''
                  CREATE TABLE IF NOT EXISTS carpetas (
                                                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                          nombre TEXT UNIQUE NOT NULL
                  )
                  ''')
        c.execute('''
                  CREATE TABLE IF NOT EXISTS palabra_carpeta (
                                                                 palabra TEXT,
                                                                 carpeta_id INTEGER,
                                                                 FOREIGN KEY(palabra) REFERENCES palabras(palabra),
                      FOREIGN KEY(carpeta_id) REFERENCES carpetas(id)
                      )
                  ''')
        conn.commit()
        conn.close()

    def create_menu(self):
        menubar = tk.Menu(self.master)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Exportar a CSV", command=self.export_to_csv)
        file_menu.add_command(label="Exportar a PDF", command=self.export_to_pdf)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.master.quit)
        menubar.add_cascade(label="Archivo", menu=file_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Acerca de", command=lambda: messagebox.showinfo(
            "Acerca de", "📒 Diccionario Inteligente v3.0\nDesarrollado por TeCaHerDev 😊"))
        menubar.add_cascade(label="Ayuda", menu=help_menu)

        self.master.config(menu=menubar)

    def show_status(self, message, duration=3000):
        """Mostrar mensaje temporal en la etiqueta de estado"""
        self.status_label.config(text=message)
        self.master.after(duration, lambda: self.status_label.config(text=""))

    def translate_word(self):
        """Traducir palabra actual con GoogleTranslator"""
        if not self.current_word:
            return
        try:
            translated = GoogleTranslator(source='en', target='es').translate(self.current_word)
            messagebox.showinfo("Traducción", f"{self.current_word} ➡️ {translated}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo traducir la palabra.\n{e}")

    def load_words(self):
        self.words.clear()
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT palabra, definicion, sinonimos FROM palabras")
        for palabra, definicion, sinonimos in c.fetchall():
            self.words[palabra] = {
                "definition": definicion,
                "synonyms": sinonimos.split(", ") if sinonimos else []
            }
        conn.close()
        self.update_word_listbox()

    def create_widgets(self):
        main_frame = ttk.Frame(self.master, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.status_label = ttk.Label(main_frame, text="", foreground="green")
        self.status_label.pack(pady=(0, 5))

        search_frame = ttk.LabelFrame(main_frame, text="🔍 Buscar palabra")
        search_frame.pack(fill=tk.X, pady=5)
        self.search_entry = ttk.Entry(search_frame, width=40)
        self.search_entry.pack(side=tk.LEFT, padx=5, pady=5)
        self.search_button = ttk.Button(search_frame, text="🔎", command=self.search_word, bootstyle=PRIMARY)
        self.search_button.pack(side=tk.LEFT, padx=5)

        self.word_listbox = tk.Listbox(main_frame, selectmode=tk.EXTENDED, height=6)
        self.word_listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        self.word_listbox.bind('<<ListboxSelect>>', self.on_word_select)

        action_frame = ttk.Frame(main_frame)
        action_frame.pack(pady=10)
        ttk.Button(action_frame, text="♻📂 Mover a la carpeta...", command=self.move_words).pack(side=tk.LEFT, padx=5)

        self.definition_text = tk.Text(main_frame, height=5, wrap=tk.WORD)
        self.definition_text.pack(fill=tk.BOTH, expand=True, pady=(10,5))
        self.definition_text.config(state='disabled')
        self.synonyms_text = tk.Text(main_frame, height=4, wrap=tk.WORD)
        self.synonyms_text.pack(fill=tk.BOTH, expand=True)
        self.synonyms_text.config(state='disabled')

        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=5)
        self.edit_button = ttk.Button(btn_frame, text="🖊️ Editar", command=self.edit_word,
                                      state='disabled', bootstyle=WARNING)
        self.edit_button.pack(side=tk.LEFT, padx=5)
        self.save_button = ttk.Button(btn_frame, text="💾 Guardar", command=self.save_changes,
                                      state='disabled', bootstyle=SUCCESS)
        self.save_button.pack(side=tk.LEFT, padx=5)
        self.delete_button = ttk.Button(btn_frame, text="❌ Eliminar", command=self.delete_word,
                                        state='disabled', bootstyle=DANGER)
        self.delete_button.pack(side=tk.LEFT, padx=5)
        self.pronounce_button = ttk.Button(btn_frame, text="🔊 Pronunciar", command=self.pronounce_word,
                                           bootstyle=INFO)
        self.pronounce_button.pack(side=tk.LEFT, padx=5)
        self.translate_button = ttk.Button(btn_frame, text="🌐 Traducir", command=self.translate_word,
                                           bootstyle=LIGHT)
        self.translate_button.pack(side=tk.LEFT, padx=5)

        folder_frame = ttk.LabelFrame(self.master, text="📁 Carpetas")
        folder_frame.pack(fill=tk.X, padx=10, pady=5)
        self.folder_var = tk.StringVar()
        self.folder_combo = ttk.Combobox(folder_frame, textvariable=self.folder_var,
                                         state='readonly')
        self.folder_combo.pack(side=tk.LEFT, padx=5)
        self.folder_combo.bind('<<ComboboxSelected>>', lambda e: self.load_words_by_folder())
        ttk.Button(folder_frame, text="➕ Crear", command=self.add_folder).pack(side=tk.LEFT, padx=5)
        ttk.Button(folder_frame, text="✏️ Renombrar", command=self.rename_folder).pack(side=tk.LEFT, padx=5)
        ttk.Button(folder_frame, text="🗑️ Eliminar", command=self.delete_folder).pack(side=tk.LEFT, padx=5)
        self.load_folders()

    def load_folders(self):
        """Cargar nombres de carpetas"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT nombre FROM carpetas ORDER BY nombre")
        carpetas = [row[0] for row in c.fetchall()]
        conn.close()
        self.folder_combo['values'] = ['Todas'] + carpetas
        self.folder_combo.set('Todas')

    def add_folder(self):
        """Añadir nueva carpeta"""
        nombre = simpledialog.askstring("Nueva carpeta", "Nombre de la carpeta:")
        if not nombre:
            return
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        try:
            c.execute("INSERT INTO carpetas (nombre) VALUES (?)", (nombre,))
            conn.commit()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Ya existe carpeta con ese nombre.")
        conn.close()
        self.load_folders()

    def rename_folder(self):
        """Renombrar carpeta seleccionada"""
        vieja = self.folder_var.get()
        if vieja == 'Todas':
            return
        nueva = simpledialog.askstring("Renombrar carpeta", "Nuevo nombre:", initialvalue=vieja)
        if not nueva:
            return
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("UPDATE carpetas SET nombre=? WHERE nombre=?", (nueva, vieja))
        conn.commit()
        conn.close()
        self.load_folders()

    def delete_folder(self):
        """Eliminar carpeta y asociaciones"""
        nombre = self.folder_var.get()
        if nombre == 'Todas':
            return
        if not messagebox.askyesno("Confirmar", f"¿Eliminar carpeta '{nombre}'?"):
            return
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT id FROM carpetas WHERE nombre=?", (nombre,))
        row = c.fetchone()
        if row:
            cid = row[0]
            c.execute("DELETE FROM palabra_carpeta WHERE carpeta_id=?", (cid,))
            c.execute("DELETE FROM carpetas WHERE id=?", (cid,))
            conn.commit()
        conn.close()
        self.load_folders()
        self.load_words()

    def load_words_by_folder(self):
        """Cargar palabras según la carpeta seleccionada"""
        self.words.clear()
        sel = self.folder_var.get()
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        if sel == 'Todas':
            c.execute("SELECT palabra, definicion, sinonimos FROM palabras")
        else:
            c.execute("SELECT id FROM carpetas WHERE nombre=?", (sel,))
            fid = c.fetchone()[0]
            c.execute('''
                      SELECT p.palabra, p.definicion, p.sinonimos
                      FROM palabras p
                               JOIN palabra_carpeta pc ON p.palabra=pc.palabra
                      WHERE pc.carpeta_id=?
                      ''', (fid,))
        for p, d, s in c.fetchall():
            self.words[p] = {"definition": d, "synonyms": s.split(", ") if s else []}
        conn.close()
        self.update_word_listbox()

    def save_to_db(self, palabra, definicion, sinonimos, carpeta=None):
        """Guardar o actualizar palabra y su carpeta (si aplica)"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        # Insertar/actualizar en palabras
        c.execute("REPLACE INTO palabras (palabra, definicion, sinonimos) VALUES (?, ?, ?)",
                  (palabra, definicion, ", ".join(sinonimos)))
        # Quitar asociaciones previas
        c.execute("DELETE FROM palabra_carpeta WHERE palabra=?", (palabra,))
        # Asignar nueva carpeta si válida
        if carpeta and carpeta != 'Todas':
            c.execute("SELECT id FROM carpetas WHERE nombre=?", (carpeta,))
            r = c.fetchone()
            if r:
                c.execute("INSERT INTO palabra_carpeta (palabra, carpeta_id) VALUES (?, ?)",
                          (palabra, r[0]))
        conn.commit()
        conn.close()

    def search_word(self):
        """Buscar palabra en web/nltk y guardarla"""
        w = self.search_entry.get().strip().lower()
        if not w:
            return
        defin = self.scrape_definition(w) or self.nltk_definition(w)
        syns = self.scrape_synonyms(w) or self.nltk_synonyms(w)
        if not defin:
            messagebox.showinfo("Sin resultados", "No se encontró definición.")
            return
        self.words[w] = {"definition": defin, "synonyms": syns}
        # Si estamos en 'Todas', preguntar carpeta destino
        # Siempre guardar en la carpeta principal (Todas)
        carpeta = None

    # Guardar
        self.save_to_db(w, defin, syns, carpeta)
        self.update_word_listbox()
        self.display_word(w)
        self.show_status("Palabra añadida con éxito")

    def nltk_definition(self, word):
        synsets = wordnet.synsets(word)
        return synsets[0].definition() if synsets else ''

    def nltk_synonyms(self, word):
        synsets = wordnet.synsets(word)
        if not synsets:
            return []
        return list({lem.name().replace('_',' ') for syn in synsets for lem in syn.lemmas()})[:5]

    def scrape_definition(self, word):
        try:
            url = f"https://dictionary.cambridge.org/es/diccionario/ingles/{word}"
            res = requests.get(url, headers={'User-Agent':'Mozilla/5.0'})
            soup = BeautifulSoup(res.content, 'html.parser')
            d = soup.find('div', class_='def ddef_d db')
            return d.text.strip() if d else ''
        except:
            return ''

    def scrape_synonyms(self, word):
        try:
            url = f"https://www.thesaurus.com/browse/{word}"
            res = requests.get(url, headers={'User-Agent':'Mozilla/5.0'})
            soup = BeautifulSoup(res.text, 'html.parser')
            syns = []
            for a in soup.find_all('a', href=True):
                if '/browse/' in a['href'] and a.text.strip().lower()!=word:
                    syns.append(a.text.strip())
                if len(syns)>=5:
                    break
            return syns
        except:
            return []

    def update_word_listbox(self):
        self.word_listbox.delete(0, tk.END)
        for w in sorted(self.words):
            self.word_listbox.insert(tk.END, w)

    def display_word(self, w):
        self.current_word = w
        self.definition_text.config(state='normal')
        self.synonyms_text.config(state='normal')
        self.definition_text.delete('1.0', tk.END)
        self.synonyms_text.delete('1.0', tk.END)
        self.definition_text.insert(tk.END, self.words[w]['definition'])
        self.synonyms_text.insert(tk.END, ', '.join(self.words[w]['synonyms']))
        self.definition_text.config(state='disabled')
        self.synonyms_text.config(state='disabled')
        self.edit_button.config(state='normal')
        self.delete_button.config(state='normal')
        self.save_button.config(state='disabled')

    def on_word_select(self, event):
        if sel:=self.word_listbox.curselection():
            w = self.word_listbox.get(sel[0])
            self.display_word(w)

    def edit_word(self):
        self.definition_text.config(state='normal')
        self.synonyms_text.config(state='normal')
        self.save_button.config(state='normal')

    def save_changes(self):
        if not self.current_word:
            return
        d = self.definition_text.get('1.0', tk.END).strip()
        s = self.synonyms_text.get('1.0', tk.END).strip().split(', ')
        carpeta = self.folder_var.get()
        carpeta = carpeta if carpeta!='Todas' else None
        self.save_to_db(self.current_word, d, s, carpeta)
        self.definition_text.config(state='disabled')
        self.synonyms_text.config(state='disabled')
        self.save_button.config(state='disabled')
        self.show_status('Cambios guardados')

    def move_words(self):
        sel = self.word_listbox.curselection()
        if not sel:
            return
        dest = simpledialog.askstring('Mover a carpeta','Nombre de carpeta destino:')
        if not dest or dest not in self.folder_combo['values'] or dest=='Todas':
            messagebox.showinfo('Mover palabras','Carpeta no válida.')
            return
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT id FROM carpetas WHERE nombre=?",(dest,))
        row=c.fetchone()
        if not row:
            messagebox.showerror('Error','Carpeta no encontrada.')
            conn.close()
            return
        fid=row[0]
        for i in sel:
            w=self.word_listbox.get(i)
            c.execute("DELETE FROM palabra_carpeta WHERE palabra=?",(w,))
            c.execute("INSERT INTO palabra_carpeta (palabra,carpeta_id) VALUES (?,?)",(w,fid))
        conn.commit()
        conn.close()
        self.show_status(f'Palabras movidas → {dest}')
        self.load_words_by_folder()

    def delete_word(self):
        if not self.current_word:
            return
        if not messagebox.askyesno('Eliminar palabra',f"¿Eliminar '{self.current_word}'? ⚠️"):
            return
        conn=sqlite3.connect(self.db_path);
        c=conn.cursor()
        c.execute("DELETE FROM palabras WHERE palabra=?",(self.current_word,))
        c.execute("DELETE FROM palabra_carpeta WHERE palabra=?",(self.current_word,))
        conn.commit();conn.close()
        del self.words[self.current_word]
        self.update_word_listbox()
        self.definition_text.config(state='normal');self.synonyms_text.config(state='normal')
        self.definition_text.delete('1.0',tk.END);self.synonyms_text.delete('1.0',tk.END)
        self.definition_text.config(state='disabled');self.synonyms_text.config(state='disabled')
        self.edit_button.config(state='disabled');self.delete_button.config(state='disabled')
        self.current_word=''
        self.show_status('Palabra eliminada🆗')

    def export_to_csv(self):
        path=filedialog.asksaveasfilename(defaultextension='.csv',filetypes=[('CSV','*.csv')])
        if not path: return
        with open(path,'w',newline='',encoding='utf-8') as f:
            w=csv.writer(f)
            w.writerow(['Palabra','Definición','Sinónimos'])
            for p,d in self.words.items():
                w.writerow([p,d['definition'],', '.join(d['synonyms'])])
        self.show_status('Exportado a CSV')

    def export_to_pdf(self):
        try:
            path = filedialog.asksaveasfilename(
                defaultextension='.pdf',
                filetypes=[('PDF', '*.pdf')]
            )
            if not path:
                return

            pdf = FPDF()
            pdf.set_margins(20, 20, 20)
            pdf.set_auto_page_break(True, 15)
            pdf.add_page()

            # Registrar la fuente Arial (regular y negrita)
            pdf.add_font('Arial', '', r'C:\Windows\Fonts\arial.ttf', uni=True)
            pdf.add_font('Arial', 'B', r'C:\Windows\Fonts\arial.ttf', uni=True)

            for palabra, datos in sorted(self.words.items()):
                # Imprimir la palabra en negrita
                pdf.set_font('Arial', 'B', 14)
                pdf.cell(0, 10, txt=palabra.capitalize(), ln=True)
                pdf.ln(2)

                # Volver a fuente regular para definición y sinónimos
                pdf.set_font('Arial', '', 12)
                definicion = datos['definition'].replace('\n', ' ')
                pdf.multi_cell(0, 6, txt=f"Definición: {definicion}")
                pdf.ln(2)

                sinonimos = ', '.join(datos['synonyms']).replace('\n', ' ')
                pdf.multi_cell(0, 6, txt=f"Sinónimos: {sinonimos}")
                pdf.ln(10)

            pdf.output(path)
            messagebox.showinfo('Éxito', '✅ PDF exportado correctamente')

        except Exception as e:
            messagebox.showerror('Error', f'❌ No se pudo exportar el PDF.\nError: {e}')


    def pronounce_word(self):
        if not self.current_word: return
        tts=gTTS(text=self.current_word,lang='en');temp='temp.mp3';tts.save(temp)
        playsound(temp);os.remove(temp)

if __name__=='__main__':
    root=tb.Window(themename='superhero')
    app=SmartDictionaryApp(root)
    root.mainloop()
