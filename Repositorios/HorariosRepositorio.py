import pyodbc
from Entidades.Horarios import Horarios
from Utilidades.Configuracion import Configuracion

class HorariosRepositorio:
    def __init__(self):
        self.conn = Configuracion.obtener_conexion()
        self.cursor = self.conn.cursor()

    def obtener_todos(self):
        """Obtiene todos los horarios"""
        self.cursor.execute("{CALL ObtenerHorarios()}")
        results = self.cursor.fetchall()

        horarios = []
        for row in results:
            horario = self._mapear_fila_a_horario(row)
            horarios.append(horario)

        return horarios

    def obtener_por_id(self, horario_id: int) -> Horarios:
        """Obtiene un horario específico por su ID"""
        self.cursor.execute("{CALL ObtenerHorarioPorID(?)}", horario_id)
        row = self.cursor.fetchone()

        if not row:
            return None

        return self._mapear_fila_a_horario(row)

    def crear(self, horario: Horarios) -> int:
        self.cursor.execute(
            "{CALL CrearHorario(?, ?, ?, ?)}",
            (
                horario.GetDia_semana(),
                horario.GetHora_inicio(),
                horario.GetHora_fin(),
                horario.GetMax_voluntarios()
            )
        )
        row = self.cursor.fetchone()
        if row:
            return row[0]  # nuevo_id
        else:
            return None


    def actualizar(self, horario: Horarios) -> bool:
        """Actualiza la información de un horario existente"""
        self.cursor.execute(
            "{CALL ActualizarHorario(?, ?, ?, ?, ?)}",
            (
                horario.GetId(),
                horario.GetDia_semana(),
                horario.GetHora_inicio(),
                horario.GetHora_fin(),
                horario.GetMax_voluntarios()
            )
        )
        self.conn.commit()
        return self.cursor.rowcount > 0

    def eliminar(self, horario_id: int) -> bool:
        """Elimina un horario de la base de datos"""
        self.cursor.execute("{CALL EliminarHorario(?)}", horario_id)
        self.conn.commit()
        return self.cursor.rowcount > 0

    def _mapear_fila_a_horario(self, row) -> Horarios:
        """Mapea una fila de resultado a un objeto Horarios"""
        horario = Horarios()
        horario.SetId(row[0])
        horario.SetDia_semana(row[1])
        horario.SetHora_inicio(str(row[2]))
        horario.SetHora_fin(str(row[3]))
        horario.SetMax_voluntarios(row[4])
        return horario

    def cerrar_conexion(self):
        """Cierra la conexión a la base de datos"""
        self.cursor.close()
        self.conn.close()
