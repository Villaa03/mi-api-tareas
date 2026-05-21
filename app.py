from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

tareas = [
    {"id": 1, "titulo": "Comprar mercado", "completada": False, "creada": "2025-01-01"},
    {"id": 2, "titulo": "Hacer ejercicio", "completada": False, "creada": "2025-01-01"},
    {"id": 3, "titulo": "Leer un libro", "completada": True, "creada": "2025-01-01"},
]
contador_id = 4


@app.route("/", methods=["GET"])
def inicio():
    return jsonify({
        "mensaje": "API de Tareas",
        "version": "1.0.0"
    })


@app.route("/tareas", methods=["GET"])
def obtener_tareas():
    return jsonify({"total": len(tareas), "tareas": tareas}), 200


@app.route("/tareas/<int:tarea_id>", methods=["GET"])
def obtener_tarea(tarea_id):
    tarea = next((t for t in tareas if t["id"] == tarea_id), None)
    if tarea is None:
        return jsonify({"error": f"Tarea {tarea_id} no encontrada"}), 404
    return jsonify(tarea), 200


@app.route("/tareas", methods=["POST"])
def crear_tarea():
    global contador_id
    datos = request.get_json()
    if not datos or "titulo" not in datos:
        return jsonify({"error": "El campo 'titulo' es obligatorio"}), 400
    nueva_tarea = {
        "id": contador_id,
        "titulo": datos["titulo"],
        "completada": datos.get("completada", False),
        "creada": datetime.now().strftime("%Y-%m-%d"),
    }
    tareas.append(nueva_tarea)
    contador_id += 1
    return jsonify({"mensaje": "Tarea creada", "tarea": nueva_tarea}), 201


@app.route("/tareas/<int:tarea_id>", methods=["PUT"])
def actualizar_tarea(tarea_id):
    tarea = next((t for t in tareas if t["id"] == tarea_id), None)
    if tarea is None:
        return jsonify({"error": f"Tarea {tarea_id} no encontrada"}), 404
    datos = request.get_json()
    if "titulo" in datos:
        tarea["titulo"] = datos["titulo"]
    if "completada" in datos:
        tarea["completada"] = datos["completada"]
    return jsonify({"mensaje": "Tarea actualizada", "tarea": tarea}), 200


@app.route("/tareas/<int:tarea_id>", methods=["DELETE"])
def eliminar_tarea(tarea_id):
    global tareas
    tarea = next((t for t in tareas if t["id"] == tarea_id), None)
    if tarea is None:
        return jsonify({"error": f"Tarea {tarea_id} no encontrada"}), 404
    tareas = [t for t in tareas if t["id"] != tarea_id]
    return jsonify({"mensaje": f"Tarea {tarea_id} eliminada"}), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
