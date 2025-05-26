from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from Repositorios.RefugiosRepositorio import RefugiosRepositorio
from Entidades.Refugios import Refugios

refugios_bp = Blueprint('refugios_bp', __name__)

# ✅ Listar refugios (sin token)
@refugios_bp.route('/refugios', methods=['GET'])
def obtener_refugios():
    repo = RefugiosRepositorio()
    refugios = repo.obtener_todos()

    resultado = []
    for r in refugios:
        resultado.append({
            "id": r.GetId(),
            "nombre": r.GetNombre(),
            "direccion": r.GetDireccion(),
            "telefono": r.GetTelefono(),
            "correo": r.GetCorreo()
        })

    return jsonify(resultado)

# ✅ Obtener un refugio por ID (requiere token)
@refugios_bp.route('/refugios/<int:refugio_id>', methods=['GET'])
@jwt_required()
def obtener_refugio_por_id(refugio_id):
    repo = RefugiosRepositorio()
    refugio = repo.obtener_por_id(refugio_id)

    if not refugio:
        return jsonify({"msg": "Refugio no encontrado"}), 404

    return jsonify({
        "id": refugio.GetId(),
        "nombre": refugio.GetNombre(),
        "direccion": refugio.GetDireccion(),
        "telefono": refugio.GetTelefono(),
        "correo": refugio.GetCorreo()
    })

# ✅ Crear refugio (requiere token)
@refugios_bp.route('/refugios', methods=['POST'])
@jwt_required()
def crear_refugio():
    data = request.get_json()
    refugio = Refugios()
    refugio.SetNombre(data.get("nombre"))
    refugio.SetDireccion(data.get("direccion"))
    refugio.SetTelefono(data.get("telefono"))
    refugio.SetCorreo(data.get("correo"))

    repo = RefugiosRepositorio()
    nuevo_id = repo.crear(refugio)

    return jsonify({"msg": "Refugio creado", "id": nuevo_id}), 201

# ✅ Actualizar refugio (requiere token)
@refugios_bp.route('/refugios/<int:refugio_id>', methods=['PUT'])
@jwt_required()
def actualizar_refugio(refugio_id):
    repo = RefugiosRepositorio()
    refugio = repo.obtener_por_id(refugio_id)

    if not refugio:
        return jsonify({"msg": "Refugio no encontrado"}), 404

    data = request.get_json()
    refugio.SetNombre(data.get("nombre", refugio.GetNombre()))
    refugio.SetDireccion(data.get("direccion", refugio.GetDireccion()))
    refugio.SetTelefono(data.get("telefono", refugio.GetTelefono()))
    refugio.SetCorreo(data.get("correo", refugio.GetCorreo()))

    if repo.actualizar(refugio):
        return jsonify({"msg": "Refugio actualizado"}), 200
    else:
        return jsonify({"msg": "Error al actualizar"}), 500

# ✅ Eliminar refugio (requiere token)
@refugios_bp.route('/refugios/<int:refugio_id>', methods=['DELETE'])
@jwt_required()
def eliminar_refugio(refugio_id):
    repo = RefugiosRepositorio()
    if repo.eliminar(refugio_id):
        return jsonify({"msg": "Refugio eliminado"}), 200
    else:
        return jsonify({"msg": "Error al eliminar o refugio no encontrado"}), 404
