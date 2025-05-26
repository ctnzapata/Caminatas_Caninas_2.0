from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from Repositorios.HistorialCaminatasRepositorio import HistorialCaminatasRepositorio
from Entidades.HistorialCaminatas import HistorialCaminatas

historial_bp = Blueprint('historial_bp', __name__)

# ✅ Listar historial de caminatas (público)
@historial_bp.route('/historial-caminatas', methods=['GET'])
def listar_historial():
    repo = HistorialCaminatasRepositorio()
    caminatas = repo.obtener_todos()

    resultado = []
    for c in caminatas:
        resultado.append({
            "id": c.GetId(),
            "registro_caminata_id": c.GetRegistro_caminata_id(),
            "duracion_real_min": c.GetDuracion_real_min(),
            "distancia_real_km": c.GetDistancia_real_km(),
            "comportamiento_perro": c.GetComportamiento_perro(),
            "observaciones": c.GetObservaciones()
        })

    return jsonify(resultado)

# ✅ Crear historial de caminata (requiere autenticación)
@historial_bp.route('/historial-caminatas', methods=['POST'])
@jwt_required()
def crear_historial():
    data = request.get_json()
    caminata = HistorialCaminatas()
    caminata.SetRegistro_caminata_id(data.get("registro_caminata_id"))
    caminata.SetDuracion_real_min(data.get("duracion_real_min"))
    caminata.SetDistancia_real_km(data.get("distancia_real_km"))
    caminata.SetComportamiento_perro(data.get("comportamiento_perro").lower())
    caminata.SetObservaciones(data.get("observaciones"))

    repo = HistorialCaminatasRepositorio()
    nuevo_id = repo.crear(caminata)

    return jsonify({"msg": "Historial creado", "id": nuevo_id}), 201

# ✅ Actualizar historial de caminata (requiere autenticación)
@historial_bp.route('/historial-caminatas/<int:id_caminata>', methods=['PUT'])
@jwt_required()
def actualizar_historial(id_caminata):
    repo = HistorialCaminatasRepositorio()
    caminata = repo.obtener_por_id(id_caminata)

    if not caminata:
        return jsonify({"msg": "Historial no encontrado"}), 404

    data = request.get_json()
    caminata.SetRegistro_caminata_id(data.get("registro_caminata_id", caminata.GetRegistro_caminata_id()))
    caminata.SetDuracion_real_min(data.get("duracion_real_min", caminata.GetDuracion_real_min()))
    caminata.SetDistancia_real_km(data.get("distancia_real_km", caminata.GetDistancia_real_km()))
    caminata.SetComportamiento_perro(data.get("comportamiento_perro", caminata.GetComportamiento_perro()).lower())
    caminata.SetObservaciones(data.get("observaciones", caminata.GetObservaciones()))

    if repo.actualizar(caminata):
        return jsonify({"msg": "Historial actualizado"}), 200
    else:
        return jsonify({"msg": "Error al actualizar el historial"}), 500

# ✅ Eliminar historial de caminata (requiere autenticación)
@historial_bp.route('/historial-caminatas/<int:id_caminata>', methods=['DELETE'])
@jwt_required()
def eliminar_historial(id_caminata):
    repo = HistorialCaminatasRepositorio()
    if repo.eliminar(id_caminata):
        return jsonify({"msg": "Historial eliminado"}), 200
    else:
        return jsonify({"msg": "Historial no encontrado o error al eliminar"}), 404

# ✅ Obtener historial por ID (requiere autenticación)
@historial_bp.route('/historial-caminatas/<int:id_caminata>', methods=['GET'])
@jwt_required()
def obtener_historial(id_caminata):
    repo = HistorialCaminatasRepositorio()
    c = repo.obtener_por_id(id_caminata)
    
    if c:
        resultado = {
            "id": c.GetId(),
            "registro_caminata_id": c.GetRegistro_caminata_id(),
            "duracion_real_min": c.GetDuracion_real_min(),
            "distancia_real_km": c.GetDistancia_real_km(),
            "comportamiento_perro": c.GetComportamiento_perro(),
            "observaciones": c.GetObservaciones()
        }
        return jsonify(resultado)
    else:
        return jsonify({"msg": "Historial no encontrado"}), 404
