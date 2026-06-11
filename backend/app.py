import json
import os

from chatbot import obtener_respuesta
from flask import Flask, abort, jsonify, request, send_from_directory, session
from flask_cors import CORS


RUTA_FRONTEND = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Frontend"))

app = Flask(__name__, static_folder=RUTA_FRONTEND, static_url_path="")
app.config.update(
    SECRET_KEY=os.environ.get("CHATBOT_SECRET_KEY", "renzo-costa-tesis-desarrollo"),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax"
)

CORS(app, supports_credentials=True)


@app.route("/", methods=["GET"])
def frontend():
    return send_from_directory(RUTA_FRONTEND, "index.html")


@app.route("/api/status", methods=["GET"])
def inicio():
    return jsonify({
        "mensaje": "API del Chatbot Renzo Costa activa correctamente.",
        "estado": "online"
    })


@app.route("/chat", methods=["POST"])
def chat():
    try:
        datos = request.get_json()

        if not datos:
            return jsonify({"error": "No se recibieron datos JSON."}), 400

        mensaje_usuario = datos.get("mensaje", "").strip()

        if not mensaje_usuario:
            return jsonify({
                "respuesta": "Por favor escribe una consulta para poder ayudarte.",
                "intencion": "vacio"
            }), 200

        contexto = session.get("chat_contexto", {})
        resultado = obtener_respuesta(mensaje_usuario, contexto=contexto)

        session["chat_contexto"] = resultado.pop("contexto", contexto)
        session.modified = True

        print("=" * 50)
        print(f"Mensaje recibido: {mensaje_usuario}")
        print(f"Intencion detectada: {resultado['intencion']}")
        print(f"Respuesta enviada: {resultado['respuesta']}")
        print("=" * 50)

        return jsonify(resultado), 200
    except Exception as e:
        print(f"ERROR EN /chat: {str(e)}")
        return jsonify({
            "respuesta": "Ocurrio un error interno en el servidor.",
            "intencion": "error"
        }), 500


@app.route("/session/reset", methods=["POST"])
def reiniciar_sesion():
    session.pop("chat_contexto", None)
    return jsonify({"mensaje": "Contexto de conversacion reiniciado."}), 200


@app.route("/metrics", methods=["GET"])
def obtener_metricas():
    clave_metricas = os.environ.get("METRICS_ACCESS_KEY")

    if not clave_metricas or request.args.get("key") != clave_metricas:
        abort(404)

    try:
        ruta_metricas = os.path.join(os.path.dirname(__file__), "metrics.json")

        with open(ruta_metricas, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        return jsonify(datos), 200
    except FileNotFoundError:
        return jsonify({"error": "No se encontro metrics.json"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("=" * 60)
    print("CHATBOT RENZO COSTA - SERVIDOR FLASK")
    print("=" * 60)
    print("Servidor iniciado correctamente")
    print("URL local: http://localhost:5000")
    print("Endpoints disponibles:")
    print("GET  /")
    print("GET  /api/status")
    print("POST /chat")
    print("POST /session/reset")
    print("=" * 60)

    app.run(debug=True, host="0.0.0.0", port=5000, threaded=True)
