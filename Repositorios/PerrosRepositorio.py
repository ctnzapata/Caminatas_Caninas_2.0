import pyodbc
from Entidades.Perros import Perros
from Entidades.Refugios import Refugios
from Utilidades.Configuracion import Configuracion

class PerrosRepositorio:
    def __init__(self):
        self.conn = Configuracion.obtener_conexion()
        self.cursor = self.conn.cursor()

    def obtener_todos(self):
        """Obtiene todos los perros con información de sus refugios"""
        self.cursor.execute("{CALL ObtenerPerrosCompletos()}")
        results = self.cursor.fetchall()

        perros = []
        for row in results:
            perro = self._mapear_fila_a_perro(row)
            perros.append(perro)

        return perros

    def obtener_por_id(self, perro_id: int) -> Perros:
        """Obtiene un perro específico por su ID"""
        self.cursor.execute("{CALL ObtenerPerroPorID(?)}", perro_id)
        row = self.cursor.fetchone()

        if not row:
            return None

        return self._mapear_fila_a_perro(row)

    def crear(self, perro: Perros) -> int:
        """Crea un nuevo perro y devuelve su ID"""
        self.cursor.execute("SET @nuevo_id = 0")
        self.cursor.execute(
            "{CALL CrearPerro(?, ?, ?, ?, ?, ?, ?, ?,@nuevo_id)}",
            (
                perro.GetNombre(),
                perro.GetEdad(),
                perro.GetRaza(),
                perro.GetTamanio(),
                perro.GetEnergia(),
                perro.GetDescripcion(),
                perro.GetEstado(),
                perro.GetRefugio()
            )
        )
        self.cursor.execute("SELECT @nuevo_id")
        nuevo_id = self.cursor.fetchone()[0]
        self.conn.commit()
        return nuevo_id

    def actualizar(self, perro: Perros) -> bool:
        """Actualiza la información de un perro existente"""
        self.cursor.execute(
            "{CALL ActualizarPerro(?, ?, ?, ?, ?, ?, ?, ?, ?)}",
            (
                perro.GetId(),
                perro.GetNombre(),
                perro.GetEdad(),
                perro.GetRaza(),
                perro.GetTamanio(),
                perro.GetEnergia(),
                perro.GetDescripcion(),
                perro.GetEstado(),
                perro.GetRefugio()
            )
        )
        self.conn.commit()
        return self.cursor.rowcount > 0

    def eliminar(self, perro_id: int) -> bool:
        """Elimina un perro de la base de datos"""
        self.cursor.execute("{CALL EliminarPerro(?)}", perro_id)
        self.conn.commit()
        return self.cursor.rowcount > 0

    def obtener_por_refugio(self, refugio_id: int):
        """Obtiene todos los perros de un refugio específico"""
        self.cursor.execute("{CALL ObtenerPerrosPorRefugio(?)}", refugio_id)
        results = self.cursor.fetchall()

        perros = []
        for row in results:
            perro = self._mapear_fila_a_perro(row)
            perros.append(perro)

        return perros

    def _mapear_fila_a_perro(self, row) -> Perros:
        """Mapea una fila de resultado a un objeto Perro"""
        perro = Perros()
        perro.SetId(row[0])
        perro.SetNombre(row[1])
        perro.SetEdad(row[2])
        perro.SetRaza(row[3])
        perro.SetTamanio(row[4])
        perro.SetEnergia(row[5])
        perro.SetDescripcion(row[6])
        perro.SetEstado(row[7])
        perro.SetRefugio(row[8])
        
        if len(row) > 9:  # Si incluye datos del refugio
            refugio = Refugios()
            refugio.SetId(row[8])
            refugio.SetNombre(row[9])
            perro.Set_Refugio(refugio)

        return perro

    def cerrar_conexion(self):
        """Cierra la conexión a la base de datos"""
        self.cursor.close()
        self.conn.close()