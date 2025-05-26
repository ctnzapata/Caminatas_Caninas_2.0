import pyodbc
from Entidades.Equipamiento import Equipamiento
from Utilidades.Configuracion import Configuracion

class EquipamientoRepositorio:
    def __init__(self):
        self.conn = Configuracion.obtener_conexion()
        self.cursor = self.conn.cursor()

    def obtener_todos(self):
        """Obtiene todos los equipamientos"""
        self.cursor.execute("{CALL ObtenerEquipamientos()}")
        results = self.cursor.fetchall()

        equipamientos = []
        for row in results:
            equipamiento = self._mapear_fila_a_equipamiento(row)
            equipamientos.append(equipamiento)

        return equipamientos

    def obtener_por_id(self, equipamiento_id: int) -> Equipamiento:
        """Obtiene un equipamiento específico por su ID"""
        self.cursor.execute("{CALL ObtenerEquipamientoPorID(?)}", equipamiento_id)
        row = self.cursor.fetchone()

        if not row:
            return None

        return self._mapear_fila_a_equipamiento(row)

    def crear(self, equipamiento: Equipamiento) -> int:
        """Crea un nuevo equipamiento y devuelve su ID"""
        self.cursor.execute("SET @nuevo_id = 0")
        self.cursor.execute(
            "{CALL CrearEquipamiento(?, ?, ?,@nuevo_id)}",
            (
                equipamiento.GetNombre(),
                equipamiento.GetDescripcion(),
                equipamiento.GetCantidad_disponible()
            )
        )
        self.cursor.execute("SELECT @nuevo_id")
        nuevo_id = self.cursor.fetchone()[0]
        self.conn.commit()
        return nuevo_id

    def actualizar(self, equipamiento: Equipamiento) -> bool:
        """Actualiza la información de un equipamiento existente"""
        self.cursor.execute(
            "{CALL ActualizarEquipamiento(?, ?, ?, ?)}",
            (
                equipamiento.GetId(),
                equipamiento.GetNombre(),
                equipamiento.GetDescripcion(),
                equipamiento.GetCantidad_disponible()
            )
        )
        self.conn.commit()
        return self.cursor.rowcount > 0

    def eliminar(self, equipamiento_id: int) -> bool:
        """Elimina un equipamiento de la base de datos"""
        self.cursor.execute("{CALL EliminarEquipamiento(?)}", equipamiento_id)
        self.conn.commit()
        return self.cursor.rowcount > 0

    def _mapear_fila_a_equipamiento(self, row) -> Equipamiento:
        """Mapea una fila de resultado a un objeto Equipamiento"""
        equipamiento = Equipamiento()
        equipamiento.SetId(row[0])
        equipamiento.SetNombre(row[1])
        equipamiento.SetDescripcion(row[2])
        equipamiento.SetCantidad_disponible(row[3])
        return equipamiento

    def cerrar_conexion(self):
        """Cierra la conexión a la base de datos"""
        self.cursor.close()
        self.conn.close()