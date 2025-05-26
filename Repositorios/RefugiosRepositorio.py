import pyodbc
from Entidades.Refugios import Refugios
from Utilidades.Configuracion import Configuracion

class RefugiosRepositorio:
    def __init__(self):
        self.conn = Configuracion.obtener_conexion()
        self.cursor = self.conn.cursor()

    def obtener_todos(self):
        """Obtiene todos los refugios"""
        self.cursor.execute("{CALL ObtenerRefugios()}")
        results = self.cursor.fetchall()

        refugios = []
        for row in results:
            refugio = self._mapear_fila_a_refugio(row)
            refugios.append(refugio)

        return refugios

    def obtener_por_id(self, refugio_id: int) -> Refugios:
        """Obtiene un refugio específico por su ID"""
        self.cursor.execute("{CALL ObtenerRefugioPorID(?)}", refugio_id)
        row = self.cursor.fetchone()

        if not row:
            return None

        return self._mapear_fila_a_refugio(row)

    def crear(self, refugio: Refugios) -> int:
        """Crea un nuevo refugio y devuelve su ID"""
        self.cursor.execute("SET @nuevo_id = 0")
        self.cursor.execute(
            "{CALL CrearRefugio(?, ?, ?, ?,@nuevo_id)}",
            (
                refugio.GetNombre(),
                refugio.GetDireccion(),
                refugio.GetTelefono(),
                refugio.GetCorreo()
            )
        )
        self.cursor.execute("SELECT @nuevo_id")
        nuevo_id = self.cursor.fetchone()[0]
        self.conn.commit()
        return nuevo_id

    def actualizar(self, refugio: Refugios) -> bool:
        """Actualiza la información de un refugio existente"""
        self.cursor.execute(
            "{CALL ActualizarRefugio(?, ?, ?, ?, ?)}",
            (
                refugio.GetId(),
                refugio.GetNombre(),
                refugio.GetDireccion(),
                refugio.GetTelefono(),
                refugio.GetCorreo()
            )
        )
        self.conn.commit()
        return self.cursor.rowcount > 0

    def eliminar(self, refugio_id: int) -> bool:
        """Elimina un refugio de la base de datos"""
        self.cursor.execute("{CALL EliminarRefugio(?)}", refugio_id)
        self.conn.commit()
        return self.cursor.rowcount > 0

    def _mapear_fila_a_refugio(self, row) -> Refugios:
        """Mapea una fila de resultado a un objeto Refugio"""
        refugio = Refugios()
        refugio.SetId(row[0])
        refugio.SetNombre(row[1])
        refugio.SetDireccion(row[2])
        refugio.SetTelefono(row[3])
        refugio.SetCorreo(row[4])
        return refugio

    def cerrar_conexion(self):
        """Cierra la conexión a la base de datos"""
        self.cursor.close()
        self.conn.close()