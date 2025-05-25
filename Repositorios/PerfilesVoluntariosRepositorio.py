import pyodbc
from Entidades.PerfilesVoluntarios import PerfilesVoluntarios
from Utilidades.Configuracion import Configuracion

class PerfilesVoluntariosRepositorio:
    def __init__(self):
        self.conn = Configuracion.obtener_conexion()
        self.cursor = self.conn.cursor()

    def obtener_todos(self):
        """Obtiene todos los perfiles de voluntarios"""
        self.cursor.execute("{CALL ObtenerPerfilesVoluntarios()}")
        results = self.cursor.fetchall()

        perfiles = []
        for row in results:
            perfil = self._mapear_fila_a_perfil(row)
            perfiles.append(perfil)

        return perfiles

    def obtener_por_id(self, perfil_id: int) -> PerfilesVoluntarios:
        """Obtiene un perfil específico por su ID"""
        self.cursor.execute("{CALL ObtenerPerfilVoluntarioPorID(?)}", perfil_id)
        row = self.cursor.fetchone()

        if not row:
            return None

        return self._mapear_fila_a_perfil(row)

    def crear(self, perfil: PerfilesVoluntarios) -> int:
        """Crea un nuevo perfil de voluntario y devuelve su ID"""
        self.cursor.execute(
            "{CALL CrearPerfilVoluntario(?, ?, ?, ?)}",
            (
                perfil.GetTelefono(),
                perfil.GetDireccion(),
                perfil.GetUsuario(),
                perfil.GetExperiencia()
            )
        )
        self.conn.commit()
        return self.cursor.fetchval()

    def actualizar(self, perfil: PerfilesVoluntarios) -> bool:
        """Actualiza un perfil de voluntario existente"""
        self.cursor.execute(
            "{CALL ActualizarPerfilVoluntario(?, ?, ?, ?, ?)}",
            (
                perfil.GetId(),
                perfil.GetTelefono(),
                perfil.GetDireccion(),
                perfil.GetUsuario(),
                perfil.GetExperiencia()
            )
        )
        self.conn.commit()
        return self.cursor.rowcount > 0

    def eliminar(self, perfil_id: int) -> bool:
        """Elimina un perfil de voluntario de la base de datos"""
        self.cursor.execute("{CALL EliminarPerfilVoluntario(?)}", perfil_id)
        self.conn.commit()
        return self.cursor.rowcount > 0

    def _mapear_fila_a_perfil(self, row) -> PerfilesVoluntarios:
        """Mapea una fila de resultado a un objeto PerfilesVoluntarios"""
        perfil = PerfilesVoluntarios()
        perfil.SetId(row[0])
        perfil.SetTelefono(row[1])
        perfil.SetDireccion(row[2])
        perfil.SetExperiencia(row[3])
        return perfil

    def cerrar_conexion(self):
        """Cierra la conexión a la base de datos"""
        self.cursor.close()
        self.conn.close()
