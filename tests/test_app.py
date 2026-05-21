import pytest
from app import app


@pytest.fixture
def cliente():
    app.config["TESTING"] = True
    with app.test_client() as cliente:
        yield cliente


def test_ruta_raiz(cliente):
    respuesta = cliente.get("/")
    assert respuesta.status_code == 200


def test_obtener_tareas(cliente):
    respuesta = cliente.get("/tareas")
    assert respuesta.status_code == 200
    datos = respuesta.get_json()
    assert "tareas" in datos


def test_obtener_tarea_existente(cliente):
    respuesta = cliente.get("/tareas/1")
    assert respuesta.status_code == 200
    assert respuesta.get_json()["id"] == 1


def test_obtener_tarea_inexistente(cliente):
    respuesta = cliente.get("/tareas/999")
    assert respuesta.status_code == 404


def test_crear_tarea(cliente):
    respuesta = cliente.post("/tareas", json={"titulo": "Nueva tarea"})
    assert respuesta.status_code == 201


def test_crear_tarea_sin_titulo(cliente):
    respuesta = cliente.post("/tareas", json={})
    assert respuesta.status_code == 400


def test_actualizar_tarea(cliente):
    respuesta = cliente.put("/tareas/1", json={"completada": True})
    assert respuesta.status_code == 200


def test_eliminar_tarea(cliente):
    respuesta = cliente.delete("/tareas/2")
    assert respuesta.status_code == 200
