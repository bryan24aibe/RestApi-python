from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import time
import os

app = Flask(__name__)
CORS(app)  # Habilita solicitudes CORS (opcional)

# Almacenamiento temporal de mensajes (en memoria)
messages = []

# Ruta de inicio (API)
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Bienvenido al chat REST API"}), 200

# Ruta para obtener mensajes
@app.route("/messages", methods=["GET"])
def get_messages():
    """Devuelve todos los mensajes en orden cronológico."""
    return jsonify(messages), 200

# Ruta para enviar un mensaje
@app.route("/messages", methods=["POST"])
def send_message():
    """Recibe un mensaje y lo agrega a la lista."""
    data = request.get_json()
    if not data or "username" not in data or "message" not in data:
        return jsonify({"error": "Solicitud inválida. Se requiere 'username' y 'message'."}), 400

    new_message = {
        "id": len(messages) + 1,
        "username": data["username"],
        "message": data["message"],
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    }
    messages.append(new_message)
    return jsonify(new_message), 201

# Ruta para limpiar mensajes (opcional)
@app.route("/messages", methods=["DELETE"])
def clear_messages():
    """Elimina todos los mensajes."""
    global messages
    messages = []
    return jsonify({"message": "Todos los mensajes han sido eliminados."}), 200

# Ruta para la vista HTML
@app.route("/chat", methods=["GET"])
def chat_view():
    """Devuelve una página HTML simple para interactuar con el chat."""
    return render_template("chat.html")

if __name__ == "__main__":
    # Crear carpeta de templates si no existe
    if not os.path.exists("templates"):
        os.makedirs("templates")

    app.run(debug=True)
