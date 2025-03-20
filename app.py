from flask import Flask, request, jsonify, render_template, redirect, url_for
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# Inicializar Firebase con la clave JSON
cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
glosario_ref = db.collection("glosario")  # Colección en Firestore

# Ruta para la página principal (Ver todos los términos)
@app.route("/")
def home():
    # Obtener todos los términos del glosario
    glosario = glosario_ref.stream()
    terms = []
    for doc in glosario:
        term = doc.to_dict()
        terms.append({
            'term': doc.id,  # Aquí usamos el id del documento (palabra)
            'definition': term.get('definicion')
        })
    return render_template("index.html", terms=terms)

    # Si se realiza una búsqueda, filtrar por término
    search_query = request.form.get("search")
    if search_query:
        terms = [term for term in terms if search_query.lower() in term['term'].lower()]

    # Ordenar los términos alfabéticamente
    terms.sort(key=lambda x: x['term'])

    return render_template("index.html", terms=terms)

# Ruta para agregar una palabra al glosario (Formulario)
@app.route("/agregar", methods=["POST"])
def agregar_palabra():
    palabra = request.form.get("palabra")
    definicion = request.form.get("definicion")

    if not palabra or not definicion:
        return jsonify({"error": "Faltan datos"}), 400

    # Aquí aseguramos que la palabra es el ID del documento
    glosario_ref.document(palabra).set({"definicion": definicion})

    # Redirigimos a la página principal para ver el glosario actualizado
    return redirect(url_for("home"))

# Ruta para eliminar una palabra del glosario
@app.route("/eliminar/<palabra>", methods=["GET"])
def eliminar_palabra(palabra):
    glosario_ref.document(palabra).delete()
    return redirect(url_for("home"))

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

