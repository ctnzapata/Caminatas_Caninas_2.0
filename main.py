from Repositorios.CaminatasRepositorio import CaminatasRepositorio
from Repositorios.UsuariosRepositorio import UsuariosRepositorio
from Repositorios.PerrosRepositorio import PerrosRepositorio
from Repositorios.RefugiosRepositorio import RefugiosRepositorio
from Entidades.Usuarios import Usuarios
from Entidades.Perros import Perros
from Entidades.Refugios import Refugios
import datetime

def mostrar_menu_principal():
    print("\n--- MENÚ PRINCIPAL ---")
    print("1. Consultar Caminatas")
    print("2. Gestionar Usuarios (CRUD)")
    print("3. Gestionar Perros (CRUD)")
    print("4. Gestionar Refugios (CRUD)")
    print("5. Salir")

def mostrar_menu_usuarios():
    print("\n--- GESTIÓN DE USUARIOS ---")
    print("1. Listar Usuarios")
    print("2. Agregar Usuario")
    print("3. Actualizar Usuario")
    print("4. Eliminar Usuario")
    print("5. Volver al menú principal")

def mostrar_menu_perros():
    print("\n--- GESTIÓN DE PERROS ---")
    print("1. Listar Perros")
    print("2. Agregar Perro")
    print("3. Actualizar Perro")
    print("4. Eliminar Perro")
    print("5. Buscar Perro por ID")
    print("6. Listar Perros por Refugio")
    print("7. Volver al menú principal")

def mostrar_menu_refugios():
    print("\n--- GESTIÓN DE REFUGIOS ---")
    print("1. Listar Refugios")
    print("2. Agregar Refugio")
    print("3. Actualizar Refugio")
    print("4. Eliminar Refugio")
    print("5. Buscar Refugio por ID")
    print("6. Volver al menú principal")

def consultar_caminatas():
    repo = CaminatasRepositorio()
    caminatas = repo.obtener_caminatas()

    for caminata in caminatas:
        print(f"\n--- Caminata ID: {caminata.id} ---")
        print(f"Fecha: {caminata.fecha}")
        print(f"Estado: {caminata.estado}")
        print(f"Usuario: {caminata.usuario.nombre}")
        print(f"Perro: {caminata.perro.nombre}")
        print(f"Día: {caminata.horario.dia_semana}")
        print(f"Ruta: {caminata.ruta.nombre}")

    repo.cerrar_conexion()

def gestionar_usuarios():
    repo = UsuariosRepositorio()
    
    while True:
        mostrar_menu_usuarios()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            usuarios = repo.obtener_usuarios()
            for u in usuarios:
                print(f"{u.GetId()} - {u.GetNombre()} | {u.GetCorreo()} | Rol: {u.GetRol()} | Registrado: {u.GetFecha_registro()}")
        
        elif opcion == "2":
            usuario = Usuarios()
            usuario.SetNombre(input("Nombre: "))
            usuario.SetCorreo(input("Correo: "))
            usuario.SetContrasenia(input("Contraseña: "))
            usuario.SetRol(input("Rol: "))
            usuario.SetFecha_registro(datetime.datetime.now())
            repo.insertar_usuario(usuario)
            print("✅ Usuario insertado con éxito.")

        elif opcion == "3":
            id_usuario = int(input("ID del usuario a actualizar: "))
            usuario = Usuarios()
            usuario.SetId(id_usuario)
            usuario.SetNombre(input("Nuevo nombre: "))
            usuario.SetCorreo(input("Nuevo correo: "))
            usuario.SetContrasenia(input("Nueva contraseña: "))
            usuario.SetRol(input("Nuevo rol: "))
            repo.actualizar_usuario(usuario)
            print("✅ Usuario actualizado correctamente.")
        
        elif opcion == "4":
            id_usuario = int(input("ID del usuario a eliminar: "))
            repo.eliminar_usuario(id_usuario)
            print("✅ Usuario eliminado.")
        
        elif opcion == "5":
            break
        else:
            print("❌ Opción no válida. Intente de nuevo.")
    
    repo.cerrar_conexion()

def gestionar_perros():
    repo = PerrosRepositorio()
    
    while True:
        mostrar_menu_perros()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            perros = repo.obtener_todos()
            print("\n--- LISTADO DE PERROS ---")
            for p in perros:
                refugio_nombre = p.Get_Refugio().GetNombre() if p.Get_Refugio() else "Sin refugio"
                print(f"{p.GetId()} - {p.GetNombre()} | Edad: {p.GetEdad()} | Raza: {p.GetRaza()} | Refugio: {refugio_nombre}")
        
        elif opcion == "2":
            perro = Perros()
            perro.SetNombre(input("Nombre: "))
            perro.SetEdad(int(input("Edad: ")))
            perro.SetRaza(input("Raza: "))
            perro.SetTamanio(input("Tamaño (Pequeño/Mediano/Grande): "))
            perro.SetEnergia(input("Nivel de energía (Bajo/Medio/Alto): "))
            perro.SetDescripcion(input("Descripción: "))
            perro.SetEstado(input("Estado (Disponible/Adoptado/En tratamiento): "))
            perro.SetRefugio(int(input("ID del refugio (0 si no tiene): ")))
            
            nuevo_id = repo.crear(perro)
            print(f"✅ Perro creado con ID: {nuevo_id}")

        elif opcion == "3":
            id_perro = int(input("ID del perro a actualizar: "))
            perro = repo.obtener_por_id(id_perro)
            
            if perro:
                perro.SetNombre(input(f"Nombre ({perro.GetNombre()}): ") or perro.GetNombre())
                perro.SetEdad(int(input(f"Edad ({perro.GetEdad()}): ") or perro.GetEdad()))
                perro.SetRaza(input(f"Raza ({perro.GetRaza()}): ") or perro.GetRaza())
                perro.SetTamanio(input(f"Tamaño ({perro.GetTamanio()}): ") or perro.GetTamanio())
                perro.SetEnergia(input(f"Energía ({perro.GetEnergia()}): ") or perro.GetEnergia())
                perro.SetDescripcion(input(f"Descripción ({perro.GetDescripcion()}): ") or perro.GetDescripcion())
                perro.SetEstado(input(f"Estado ({perro.GetEstado()}): ") or perro.GetEstado())
                perro.SetRefugio(int(input(f"Refugio ID ({perro.GetRefugio()}): ") or perro.GetRefugio()))
                
                if repo.actualizar(perro):
                    print("✅ Perro actualizado correctamente.")
                else:
                    print("❌ Error al actualizar el perro.")
            else:
                print("❌ Perro no encontrado.")
        
        elif opcion == "4":
            id_perro = int(input("ID del perro a eliminar: "))
            if repo.eliminar(id_perro):
                print("✅ Perro eliminado correctamente.")
            else:
                print("❌ Error al eliminar el perro o perro no encontrado.")
        
        elif opcion == "5":
            id_perro = int(input("ID del perro a buscar: "))
            perro = repo.obtener_por_id(id_perro)
            if perro:
                print("\n--- DETALLE DEL PERRO ---")
                print(f"ID: {perro.GetId()}")
                print(f"Nombre: {perro.GetNombre()}")
                print(f"Edad: {perro.GetEdad()}")
                print(f"Raza: {perro.GetRaza()}")
                print(f"Tamaño: {perro.GetTamanio()}")
                print(f"Energía: {perro.GetEnergia()}")
                print(f"Descripción: {perro.GetDescripcion()}")
                print(f"Estado: {perro.GetEstado()}")
                if perro.Get_Refugio():
                    print(f"Refugio: {perro.Get_Refugio().GetNombre()} (ID: {perro.GetRefugio()})")
                else:
                    print("Refugio: Sin refugio asignado")
            else:
                print("❌ Perro no encontrado.")
        
        elif opcion == "6":
            id_refugio = int(input("ID del refugio: "))
            perros = repo.obtener_por_refugio(id_refugio)
            if perros:
                print(f"\n--- PERROS DEL REFUGIO {id_refugio} ---")
                for p in perros:
                    print(f"{p.GetId()} - {p.GetNombre()} | Edad: {p.GetEdad()} | Raza: {p.GetRaza()}")
            else:
                print(f"ℹ️ No se encontraron perros para el refugio {id_refugio}")
        
        elif opcion == "7":
            break
        else:
            print("❌ Opción no válida. Intente de nuevo.")
    
    repo.cerrar_conexion()

def gestionar_refugios():
    repo = RefugiosRepositorio()
    
    while True:
        mostrar_menu_refugios()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            refugios = repo.obtener_todos()
            print("\n--- LISTADO DE REFUGIOS ---")
            for r in refugios:
                print(f"{r.GetId()} - {r.GetNombre()} | {r.GetDireccion()} | Tel: {r.GetTelefono()}")

        elif opcion == "2":
            refugio = Refugios()
            refugio.SetNombre(input("Nombre: "))
            refugio.SetDireccion(input("Dirección: "))
            refugio.SetTelefono(input("Teléfono: "))
            refugio.SetCorreo(input("Correo: "))
            
            nuevo_id = repo.crear(refugio)
            print(f"✅ Refugio creado con ID: {nuevo_id}")

        elif opcion == "3":
            id_refugio = int(input("ID del refugio a actualizar: "))
            refugio = repo.obtener_por_id(id_refugio)
            
            if refugio:
                refugio.SetNombre(input(f"Nombre ({refugio.GetNombre()}): ") or refugio.GetNombre())
                refugio.SetDireccion(input(f"Dirección ({refugio.GetDireccion()}): ") or refugio.GetDireccion())
                refugio.SetTelefono(input(f"Teléfono ({refugio.GetTelefono()}): ") or refugio.GetTelefono())
                refugio.SetCorreo(input(f"Correo ({refugio.GetCorreo()}): ") or refugio.GetCorreo())
                
                if repo.actualizar(refugio):
                    print("✅ Refugio actualizado correctamente.")
                else:
                    print("❌ Error al actualizar el refugio.")
            else:
                print("❌ Refugio no encontrado.")
        
        elif opcion == "4":
            id_refugio = int(input("ID del refugio a eliminar: "))
            if repo.eliminar(id_refugio):
                print("✅ Refugio eliminado correctamente.")
            else:
                print("❌ Error al eliminar el refugio o refugio no encontrado.")
        
        elif opcion == "5":
            id_refugio = int(input("ID del refugio a buscar: "))
            refugio = repo.obtener_por_id(id_refugio)
            if refugio:
                print("\n--- DETALLE DEL REFUGIO ---")
                print(f"ID: {refugio.GetId()}")
                print(f"Nombre: {refugio.GetNombre()}")
                print(f"Dirección: {refugio.GetDireccion()}")
                print(f"Teléfono: {refugio.GetTelefono()}")
                print(f"Correo: {refugio.GetCorreo()}")
            else:
                print("❌ Refugio no encontrado.")
        
        elif opcion == "6":
            break
        else:
            print("❌ Opción no válida. Intente de nuevo.")
    
    repo.cerrar_conexion()

def main():
    while True:
        mostrar_menu_principal()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            consultar_caminatas()
        elif opcion == "2":
            gestionar_usuarios()
        elif opcion == "3":
            gestionar_perros()
        elif opcion == "4":
            gestionar_refugios()
        elif opcion == "5":
            print("👋 Saliendo del sistema...")
            break
        else:
            print("❌ Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    main()