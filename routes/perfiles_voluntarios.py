from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from Repositorios.PerfilesVoluntariosRepositorio import PerfilesVoluntariosRepositorio
from Entidades.PerfilesVoluntarios import PerfilesVoluntarios

perfiles_bp = Blueprint('perfiles_bp', __name__)

# ✅ Listar perfiles de voluntarios (público)
@perfiles_bp.route('/perfiles-voluntarios', methods=['GET'])
def listar_perfiles_voluntarios():
    repo = PerfilesVoluntariosRepositorio()
    perfiles = repo.obtener_todos()

    resultado = []
    for p in perfiles:
        resultado.append({
            "id": p.GetId(),
            "usuario_id": p.GetUsuario(),
            "experiencia": p.GetExperiencia(),
            "disponibilidad": p.GetDisponibilidad()
        })

    return jsonify(resultado)

# ✅ Crear perfil de voluntario (requiere autenticación)
@perfiles_bp.route('/perfiles-voluntarios', methods=['POST'])
@jwt_required()
def crear_perfil_voluntario():
    data = request.get_json()
    perfil = PerfilesVoluntarios()
    perfil.SetUsuario(data.get("usuario_id"))
    perfil.SetExperiencia(data.get("experiencia"))
    perfil.SetDisponibilidad(data.get("disponibilidad"))

    repo = PerfilesVoluntariosRepositorio()
    nuevo_id = repo.crear(perfil)

    return jsonify({"msg": "Perfil creado", "id": nuevo_id}), 201

# ✅ Actualizar perfil de voluntario (requiere autenticación)
@perfiles_bp.route('/perfiles-voluntarios/<int:id_perfil>', methods=['PUT'])
@jwt_required()
def actualizar_perfil_voluntario(id_perfil):
    repo = PerfilesVoluntariosRepositorio()
    perfil = repo.obtener_por_id(id_perfil)

    if not perfil:
        return jsonify({"msg": "Perfil no encontrado"}), 404

    data = request.get_json()
    perfil.SetExperiencia(data.get("experiencia", perfil.GetExperiencia()))
    perfil.SetDisponibilidad(data.get("disponibilidad", perfil.GetDisponibilidad()))

    if repo.actualizar(perfil):
        return jsonify({"msg": "Perfil actualizado"}), 200
    else:
        return jsonify({"msg": "Error al actualizar el perfil"}), 500

# ✅ Eliminar perfil de voluntario (requiere autenticación)
@perfiles_bp.route('/perfiles-voluntarios/<int:id_perfil>', methods=['DELETE'])
@jwt_required()
def eliminar_perfil_voluntario(id_perfil):
    repo = PerfilesVoluntariosRepositorio()
    if repo.eliminar(id_perfil):
        return jsonify({"msg": "Perfil eliminado"}), 200
    else:
        return jsonify({"msg": "Error al eliminar el perfil o perfil no encontrado"}), 404
