from Repositorios.UsuariosRepositorio import UsuariosRepositorio

from Entidades.Usuarios import Usuarios

from routes.perros import perros_bp
from routes.caminatas import caminatas_bp
from routes.refugios import refugios_bp
from routes.equipamiento import equipamiento_bp
from routes.horarios import horarios_bp
from routes.perfiles_voluntarios import perfiles_bp
from routes.historial_caminatas import historial_bp
from routes.usuarios import usuarios_bp

import flask;
from flask import request, jsonify
from flask_jwt_extended import JWTManager, create_access_token


app = flask.Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'clave_secreta_segura'
jwt = JWTManager(app)

app.register_blueprint(perros_bp)
app.register_blueprint(caminatas_bp)
app.register_blueprint(refugios_bp)
app.register_blueprint(equipamiento_bp)
app.register_blueprint(horarios_bp)
app.register_blueprint(perfiles_bp)
app.register_blueprint(historial_bp)
app.register_blueprint(usuarios_bp)

@app.route('/')
def index():
    return jsonify({"msg": "API de caminatas comunitarias operativa 🚶‍♂️🐶"})


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    usuario = UsuariosRepositorio().buscar_usuario_por_correo(username)

    if usuario and usuario.GetContrasenia() == password:
        access_token = create_access_token(identity=usuario.GetCorreo())
        return jsonify(access_token=access_token)
    else:
        return jsonify({"msg": "Credenciales inválidas"}), 401

if __name__ == '__main__':
    app.run(debug=True)
