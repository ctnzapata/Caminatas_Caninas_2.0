from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from Repositorios.EquipamientoRepositorio import EquipamientoRepositorio
from Entidades.Equipamiento import Equipamiento

equipamiento_bp = Blueprint('equipamiento_bp', __name__)

# ✅ Listar todos los equipamientos (sin token)
@equipamiento_bp.route('/equipamientos', methods=['GET'])
def obtener_equipamientos():
    repo = EquipamientoRepositorio()
    items = repo.obtener_todos()

    resultado = []
    for e in items:
        resultado.append({
            "id": e.GetId(),
            "nombre": e.GetNombre(),
            "descripcion": e.GetDescripcion(),
            "cantidad_disponible": e.GetCantidad_disponible()
        })

    return jsonify(resultado)

# ✅ Obtener un equipamiento por ID (requiere token)
@equipamiento_bp.route('/equipamientos/<int:id_equipamiento>', methods=['GET'])
@jwt_required()
def obtener_equipamiento(id_equipamiento):
    repo = EquipamientoRepositorio()
    item = repo.obtener_por_id(id_equipamiento)

    if not item:
        return jsonify({"msg": "Equipamiento no encontrado"}), 404

    return jsonify({
        "id": item.GetId(),
        "nombre": item.GetNombre(),
        "descripcion": item.GetDescripcion(),
        "cantidad_disponible": item.GetCantidad_disponible()
    })

# ✅ Crear nuevo equipamiento (requiere token)
@equipamiento_bp.route('/equipamientos', methods=['POST'])
@jwt_required()
def crear_equipamiento():
    data = request.get_json()
    equipamiento = Equipamiento()
    equipamiento.SetNombre(data.get("nombre"))
    equipamiento.SetDescripcion(data.get("descripcion"))
    equipamiento.SetCantidad_disponible(data.get("cantidad_disponible"))

    repo = EquipamientoRepositorio()
    nuevo_id = repo.crear(equipamiento)

    return jsonify({"msg": "Equipamiento creado", "id": nuevo_id}), 201

# ✅ Actualizar equipamiento (requiere token)
@equipamiento_bp.route('/equipamientos/<int:id_equipamiento>', methods=['PUT'])
@jwt_required()
def actualizar_equipamiento(id_equipamiento):
    repo = EquipamientoRepositorio()
    item = repo.obtener_por_id(id_equipamiento)

    if not item:
        return jsonify({"msg": "Equipamiento no encontrado"}), 404

    data = request.get_json()
    item.SetNombre(data.get("nombre", item.GetNombre()))
    item.SetDescripcion(data.get("descripcion", item.GetDescripcion()))
    item.SetCantidad_disponible(data.get("cantidad_disponible", item.GetCantidad_disponible()))

    if repo.actualizar(item):
        return jsonify({"msg": "Equipamiento actualizado"}), 200
    else:
        return jsonify({"msg": "Error al actualizar"}), 500

# ✅ Eliminar equipamiento (requiere token)
@equipamiento_bp.route('/equipamientos/<int:id_equipamiento>', methods=['DELETE'])
@jwt_required()
def eliminar_equipamiento(id_equipamiento):
    repo = EquipamientoRepositorio()
    if repo.eliminar(id_equipamiento):
        return jsonify({"msg": "Equipamiento eliminado"}), 200
    else:
        return jsonify({"msg": "No se pudo eliminar o no se encontró el equipamiento"}), 404
