from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from Repositorios.CaminatasRepositorio import CaminatasRepositorio

caminatas_bp = Blueprint('caminatas_bp', __name__)

@caminatas_bp.route('/caminatas', methods=['GET'])
@jwt_required()  
def obtener_caminatas():
    repo = CaminatasRepositorio()
    caminatas = repo.obtener_caminatas()

    resultado = []
    for c in caminatas:
        resultado.append({
            "id": c.id,
            "fecha": c.fecha.strftime('%Y-%m-%d') if c.fecha else None,
            "estado": c.estado,
            "usuario": {
                "id": c.usuario.id,
                "nombre": c.usuario.nombre
            } if c.usuario else None,
            "perro": {
                "id": c.perro.id,
                "nombre": c.perro.nombre
            } if c.perro else None,
            "horario": {
                "id": c.horario.id,
                "dia_semana": c.horario.dia_semana
            } if c.horario else None,
            "ruta": {
                "id": c.ruta.id,
                "nombre": c.ruta.nombre
            } if c.ruta else None
        })

    return jsonify(resultado)
