from flask import Blueprint, request, jsonify
from Repositorios.UsuariosRepositorio import UsuariosRepositorio
from Entidades.Usuarios import Usuarios
import datetime

usuarios_bp = Blueprint('usuarios_bp', __name__, url_prefix='/usuarios')
repo = UsuariosRepositorio()

# Listar todos los usuarios
@usuarios_bp.route('/', methods=['GET'])
def listar_usuarios():
    usuarios = repo.obtener_usuarios()
    resultado = [{
        "id": u.GetId(),
        "nombre": u.GetNombre(),
        "correo": u.GetCorreo(),
        "rol": u.GetRol(),
        "fecha_registro": str(u.GetFecha_registro())
    } for u in usuarios]
    return jsonify(resultado)

# Crear un nuevo usuario
@usuarios_bp.route('/', methods=['POST'])
def crear_usuario():
    data = request.get_json()
    usuario = Usuarios()
    usuario.SetNombre(data.get("nombre"))
    usuario.SetCorreo(data.get("correo"))
    usuario.SetContrasenia(data.get("contrasenia"))
    usuario.SetRol(data.get("rol"))
    usuario.SetFecha_registro(datetime.datetime.now())
    nuevo_id = repo.insertar_usuario(usuario)
    return jsonify({"mensaje": "Usuario creado", "id": nuevo_id}), 201

# Actualizar un usuario existente
@usuarios_bp.route('/<int:id_usuario>', methods=['PUT'])
def actualizar_usuario(id_usuario):
    data = request.get_json()
    usuario = Usuarios()
    usuario.SetId(id_usuario)
    usuario.SetNombre(data.get("nombre"))
    usuario.SetCorreo(data.get("correo"))
    usuario.SetContrasenia(data.get("contrasenia"))
    usuario.SetRol(data.get("rol"))
    actualizado = repo.actualizar_usuario(usuario)
    if actualizado:
        return jsonify({"mensaje": "Usuario actualizado"})
    else:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404

# Eliminar un usuario
@usuarios_bp.route('/<int:id_usuario>', methods=['DELETE'])
def eliminar_usuario(id_usuario):
    eliminado = repo.eliminar_usuario(id_usuario)
    if eliminado:
        return jsonify({"mensaje": "Usuario eliminado"})
    else:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404
