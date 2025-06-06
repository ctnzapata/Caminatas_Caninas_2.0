import pyodbc
from Entidades.Caminatas import Caminatas
from Entidades.Usuarios import Usuarios
from Entidades.Perros import Perros
from Entidades.Horarios import Horarios
from Entidades.Rutas import Rutas
from Utilidades.Configuracion import Configuracion

class CaminatasRepositorio:
    def __init__(self):
        self.conn = Configuracion.obtener_conexion()
        self.cursor = self.conn.cursor()

    def obtener_caminatas(self):
        self.cursor.execute("{CALL obtener_caminatas_completas()}")
        results = self.cursor.fetchall()

        caminatas = []
        for row in results:
            caminata = Caminatas()
            caminata.SetId(row[0])
            caminata.SetFecha(row[1])
            caminata.SetEstado(row[2])
            
            usuario = Usuarios()
            usuario.SetNombre(row[3])
            caminata.SetUsuario(usuario)

            perro = Perros()
            perro.SetNombre(row[4])
            caminata.SetPerro(perro)

            horario = Horarios()
            horario.SetDia_semana(row[5])
            caminata.SetHorario(horario)

            ruta = Rutas()
            ruta.SetNombre(row[6])
            caminata.SetRuta(ruta)

            caminatas.append(caminata)

        return caminatas

    def cerrar_conexion(self):
        self.cursor.close()
        self.conn.close()

# # Ejemplo de uso
# if __name__ == "__main__":
#     repo = CaminatasRepositorio()
#     caminatas = repo.obtener_caminatas()

#     for caminata in caminatas:
#         print(f"Caminata {caminata.GetId()} - Fecha: {caminata.GetFecha()} - Estado: {caminata.GetEstado()}")
#         print(f"Usuario: {caminata.GetUsuario().GetNombre()}")
#         print(f"Perro: {caminata.GetPerro().GetNombre()}")
#         print(f"Horario: {caminata.GetHorario().GetDia_semana()}")
#         print(f"Ruta: {caminata.GetRuta().GetNombre()}")
#         print("---")

#     repo.cerrar_conexion()
