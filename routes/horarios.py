from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from Repositorios.HorariosRepositorio import HorariosRepositorio
from Entidades.Horarios import Horarios

horarios_bp = Blueprint('horarios_bp', __name__)

# ✅ Listar todos los horarios (sin token)
@horarios_bp.route('/horarios', methods=['GET'])
def obtener_horarios():
    repo = HorariosRepositorio()
    items = repo.obtener_todos()

    resultado = []
    for h in items:
        resultado.append({
            "id": h.GetId(),
            "dia_semana": h.GetDia_semana(),
            "hora_inicio": h.GetHora_inicio(),
            "hora_fin": h.GetHora_fin(),
            "max_voluntarios": h.GetMax_voluntarios()
        })

    return jsonify(resultado)

# ✅ Obtener un horario por ID (requiere token)
@horarios_bp.route('/horarios/<int:id_horario>', methods=['GET'])
@jwt_required()
def obtener_horario(id_horario):
    repo = HorariosRepositorio()
    horario = repo.obtener_por_id(id_horario)

    if not horario:
        return jsonify({"msg": "Horario no encontrado"}), 404

    return jsonify({
        "id": horario.GetId(),
        "dia_semana": horario.GetDia_semana(),
        "hora_inicio": horario.GetHora_inicio(),
        "hora_fin": horario.GetHora_fin(),
        "max_voluntarios": horario.GetMax_voluntarios()
    })

# ✅ Crear nuevo horario (requiere token)
@horarios_bp.route('/horarios', methods=['POST'])
@jwt_required()
def crear_horario():
    data = request.get_json()
    horario = Horarios()
    horario.SetDia_semana(data.get("dia_semana"))
    horario.SetHora_inicio(data.get("hora_inicio"))
    horario.SetHora_fin(data.get("hora_fin"))
    horario.SetMax_voluntarios(data.get("max_voluntarios"))

    repo = HorariosRepositorio()
    nuevo_id = repo.crear(horario)

    return jsonify({"msg": "Horario creado", "id": nuevo_id}), 201

# ✅ Actualizar horario (requiere token)
@horarios_bp.route('/horarios/<int:id_horario>', methods=['PUT'])
@jwt_required()
def actualizar_horario(id_horario):
    repo = HorariosRepositorio()
    horario = repo.obtener_por_id(id_horario)

    if not horario:
        return jsonify({"msg": "Horario no encontrado"}), 404

    data = request.get_json()
    horario.SetDia_semana(data.get("dia_semana", horario.GetDia_semana()))
    horario.SetHora_inicio(data.get("hora_inicio", horario.GetHora_inicio()))
    horario.SetHora_fin(data.get("hora_fin", horario.GetHora_fin()))
    horario.SetMax_voluntarios(data.get("max_voluntarios", horario.GetMax_voluntarios()))

    if repo.actualizar(horario):
        return jsonify({"msg": "Horario actualizado"}), 200
    else:
        return jsonify({"msg": "Error al actualizar el horario"}), 500

# ✅ Eliminar horario (requiere token)
@horarios_bp.route('/horarios/<int:id_horario>', methods=['DELETE'])
@jwt_required()
def eliminar_horario(id_horario):
    repo = HorariosRepositorio()
    if repo.eliminar(id_horario):
        return jsonify({"msg": "Horario eliminado"}), 200
    else:
        return jsonify({"msg": "No se pudo eliminar o no se encontró el horario"}), 404
