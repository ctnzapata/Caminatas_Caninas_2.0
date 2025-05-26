import pyodbc
from Entidades.Usuarios import Usuarios
from Utilidades.Configuracion import Configuracion
from Utilidades.Encriptado import EncriptarAES
import datetime

class UsuariosRepositorio:
    def __init__(self):
        self.conn = Configuracion.obtener_conexion()
        self.cursor = self.conn.cursor()
        self.encriptador = EncriptarAES()

    def obtener_usuarios(self):
        self.cursor.execute("{CALL obtener_usuarios()}")
        results = self.cursor.fetchall()
        usuarios = []

        for row in results:
            usuario = Usuarios()
            usuario.SetId(row[0])
            usuario.SetNombre(row[1])
            usuario.SetCorreo(row[2])
            
            try:
                contrasenia = self.encriptador.decifrar(row[3])
            except Exception:
                contrasenia = "[Error de descifrado]"

            usuario.SetContrasenia(contrasenia)
            usuario.SetRol(row[4])
            usuario.SetFecha_registro(row[5])
            usuarios.append(usuario)

        return usuarios
    
    def buscar_usuario_por_correo(self, correo):
        self.cursor.execute("{CALL buscar_usuario_por_correo(?)}", correo)
        row = self.cursor.fetchone()

        if row:
            usuario = Usuarios()
            usuario.SetId(row[0])
            usuario.SetNombre(row[1])
            usuario.SetCorreo(row[2])

            try:
                contrasenia = self.encriptador.decifrar(row[3])
            except Exception:
                contrasenia = "[Error de descifrado]"

            usuario.SetContrasenia(contrasenia)
            usuario.SetRol(row[4])
            usuario.SetFecha_registro(row[5])
            return usuario

        return None


    def insertar_usuario(self, usuario: Usuarios):
        contrasenia_cifrada = self.encriptador.cifrar(usuario.GetContrasenia())
        self.cursor.execute("{CALL insertar_usuario (?, ?, ?, ?, ?)}",
            usuario.GetNombre(),
            usuario.GetCorreo(),
            contrasenia_cifrada,
            usuario.GetRol(),
            usuario.GetFecha_registro() or datetime.datetime.now()
        )
        self.conn.commit()

    def actualizar_usuario(self, usuario: Usuarios):
        contrasenia_cifrada = self.encriptador.cifrar(usuario.GetContrasenia())
        self.cursor.execute("{CALL actualizar_usuario (?, ?, ?, ?, ?)}", 
            usuario.GetId(),
            usuario.GetNombre(),
            usuario.GetCorreo(),
            contrasenia_cifrada,
            usuario.GetRol()
        )
        self.conn.commit()

    def eliminar_usuario(self, usuario_id: int):
        self.cursor.execute("{CALL eliminar_usuario(?)}", usuario_id)
        self.conn.commit()

    def cerrar_conexion(self):
        self.cursor.close()
        self.conn.close()
