import pyodbc
from Entidades.HistorialCaminatas import HistorialCaminatas
from Utilidades.Configuracion import Configuracion

class HistorialCaminatasRepositorio:
    def __init__(self):
        self.conn = Configuracion.obtener_conexion()
        self.cursor = self.conn.cursor()

    def obtener_todos(self):
        self.cursor.execute("{CALL ObtenerHistorialCaminatas()}")
        resultados = self.cursor.fetchall()

        lista = []
        for row in resultados:
            item = self._mapear_fila(row)
            lista.append(item)
        return lista

    def obtener_por_id(self, id: int):
        self.cursor.execute("{CALL ObtenerHistorialCaminataPorID(?)}", id)
        row = self.cursor.fetchone()
        return self._mapear_fila(row) if row else None

    def crear(self, item: HistorialCaminatas) -> int:
        self.cursor.execute(
            "{CALL CrearHistorialCaminata(?, ?, ?, ?, ?, ?)}",
            (
                item.GetRegistro_caminata_id(),
                item.GetDuracion_real_min(),
                item.GetDistancia_real_km(),
                item.GetComportamiento_perro(),
                item.GetObservaciones(),
                0
            )
        )
        row = self.cursor.fetchone()
        return row[0] if row else None

    def actualizar(self, item: HistorialCaminatas) -> bool:
        self.cursor.execute(
            "{CALL ActualizarHistorialCaminata(?, ?, ?, ?, ?, ?)}",
            (
                item.GetId(),
                item.GetRegistro_caminata_id(),
                item.GetDuracion_real_min(),
                item.GetDistancia_real_km(),
                item.GetComportamiento_perro(),
                item.GetObservaciones()
            )
        )
        self.conn.commit()
        return self.cursor.rowcount > 0

    def eliminar(self, id: int) -> bool:
        self.cursor.execute("{CALL EliminarHistorialCaminata(?)}", id)
        self.conn.commit()
        return self.cursor.rowcount > 0

    def _mapear_fila(self, row):
        item = HistorialCaminatas()
        item.SetId(row[0])
        item.SetRegistro_caminata_id(row[1])
        item.SetDuracion_real_min(row[2])
        item.SetDistancia_real_km(row[3])
        item.SetComportamiento_perro(row[4])
        item.SetObservaciones(row[5])
        return item

    def cerrar_conexion(self):
        self.cursor.close()
        self.conn.close()
