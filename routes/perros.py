from flask import Blueprint, request, jsonify
from Entidades.Perros import Perros
from Repositorios.PerrosRepositorio import PerrosRepositorio
from flask_jwt_extended import jwt_required

perros_bp = Blueprint('perros', __name__)
repo = PerrosRepositorio()

@perros_bp.route('/perros', methods=['GET'])
def obtener_perros():
    perros = repo.obtener_todos()
    resultado = []
    for p in perros:
        resultado.append({
            "id": p.GetId(),
            "nombre": p.GetNombre(),
            "edad": p.GetEdad(),
            "raza": p.GetRaza(),
            "tamanio": p.GetTamanio(),
            "energia": p.GetEnergia(),
            "descripcion": p.GetDescripcion(),
            "estado": p.GetEstado(),
            "refugio": {
                "id": p.GetRefugio(),
                "nombre": p.Get_Refugio().GetNombre() if p.Get_Refugio() else None
            } if p.GetRefugio() else None
        })
    return jsonify(resultado)


@perros_bp.route('/perros/<int:id>', methods=['GET'])
def obtener_perro(id):
    perro = repo.obtener_por_id(id)
    if not perro:
        return jsonify({"error": "Perro no encontrado"}), 404

    resultado = {
        "id": perro.GetId(),
        "nombre": perro.GetNombre(),
        "edad": perro.GetEdad(),
        "raza": perro.GetRaza(),
        "tamanio": perro.GetTamanio(),
        "energia": perro.GetEnergia(),
        "descripcion": perro.GetDescripcion(),
        "estado": perro.GetEstado(),
        "refugio": {
            "id": perro.GetRefugio(),
            "nombre": perro.Get_Refugio().GetNombre() if perro.Get_Refugio() else None
        } if perro.GetRefugio() else None
    }
    return jsonify(resultado)


@perros_bp.route('/perros', methods=['POST'])
@jwt_required()
def crear_perro():
    data = request.json
    perro = Perros()
    perro.SetNombre(data.get('nombre'))
    perro.SetEdad(data.get('edad'))
    perro.SetRaza(data.get('raza'))
    perro.SetTamanio(data.get('tamanio'))
    perro.SetEnergia(data.get('energia'))
    perro.SetDescripcion(data.get('descripcion'))
    perro.SetEstado(data.get('estado'))
    perro.SetRefugio(data.get('refugio'))  # debe ser el ID del refugio o 0
    
    nuevo_id = repo.crear(perro)
    return jsonify({"mensaje": "Perro creado", "id": nuevo_id}), 201


@perros_bp.route('/perros/<int:id>', methods=['PUT'])
@jwt_required()
def actualizar_perro(id):
    data = request.json
    perro = repo.obtener_por_id(id)
    if not perro:
        return jsonify({"error": "Perro no encontrado"}), 404

    perro.SetNombre(data.get('nombre', perro.GetNombre()))
    perro.SetEdad(data.get('edad', perro.GetEdad()))
    perro.SetRaza(data.get('raza', perro.GetRaza()))
    perro.SetTamanio(data.get('tamanio', perro.GetTamanio()))
    perro.SetEnergia(data.get('energia', perro.GetEnergia()))
    perro.SetDescripcion(data.get('descripcion', perro.GetDescripcion()))
    perro.SetEstado(data.get('estado', perro.GetEstado()))
    perro.SetRefugio(data.get('refugio', perro.GetRefugio()))
    
    actualizado = repo.actualizar(perro)
    if actualizado:
        return jsonify({"mensaje": "Perro actualizado"})
    else:
        return jsonify({"error": "Error al actualizar"}), 500


@perros_bp.route('/perros/<int:id>', methods=['DELETE'])
@jwt_required()
def eliminar_perro(id):
    eliminado = repo.eliminar(id)
    if eliminado:
        return jsonify({"mensaje": "Perro eliminado"})
    else:
        return jsonify({"error": "Perro no encontrado o no se pudo eliminar"}), 404
