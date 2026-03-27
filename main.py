from services.gestion_libros import GestionLibros
from services.gestion_usuarios import GestionUsuarios  
from services.gestion_prestamos import GestionPrestamos
from services.factory_notificador import crear_notificador
from services.listar import buscar_libro_por_isbn, mostrar_prestamos_caducados, mostrar_historico

def menu():
    print("\n--- Biblioteca Digital ---")
    print("1.Añadir libro")
    print("2.Añadir usuario")
    print("3.Listar usuarios")
    print("4.Ver historial de usuario")
    print("5.Realizar préstamo")
    print("6.Devolver libro")
    print("7.Buscar libro por ISBN")
    print("8.Listar libros")
    print("9.Listar préstamos activos")
    print("10.Listar préstamos caducados no devueltos")
    print("11.Listar histórico de préstamos")
    print("12.Exportar catalogo JSON")
    print("13.Exportar catalogo CSV")
    print("14.Importar catalogo JSON")
    print("15.Importar catalogo CSV")
    print("16.Exportar usuarios JSON")
    print("17.Importar usuarios JSON")
    print("18.Exportar usuarios CSV")
    print("19.Importar usuarios CSV")
    print("20.Exportar historico de prestamos JSON")
    print("21.Importar historico de prestamos JSON")
    print("22.Exportar historico de prestamos CSV")
    print("23.Importar historico de prestamos CSV")
    print("0.Salir")

def main():
    gl = GestionLibros()
    gu = GestionUsuarios()
    gp = GestionPrestamos()
    notificador = crear_notificador("email")

    while True:
        menu()
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            titulo = input("Título del libro: ")
            autor = input("Autor del libro: ")
            isbn = input("ISBN del libro: ")
            try:
                gl.agregar_libro(titulo, autor, isbn)
                print(f"Libro '{titulo}' añadido.")
            except ValueError as e:
                print(e)
        
        elif opcion == "2":
            nombre = input("Nombre del usuario: ")
            id_usuario = int(input("ID del usuario: "))
            try:
                gu.agregar_usuario(nombre, id_usuario)
                print(f"Usuario '{nombre}' añadido.")
            except ValueError as e:
                print(e)
        elif opcion == "3":
            usuarios = gu.listar_usuarios()
            print("\nUsuarios registrados:")
            for usuario in usuarios:
                print(f"- {usuario.nombre} (ID {usuario.id_usuario})")
        elif opcion == "4":
            id_usuario = int(input("ID del usuario: "))
            try:
                usuario = gu.obtener_usuario(id_usuario)
                historial = usuario.historial()
                print(f"\nHistorial de {usuario.nombre} (ID: {usuario.id_usuario}):")
                if historial:
                    for evento in historial:
                        print(f"- {evento}")
                else:
                    print("No hay eventos registrados para este usuario.")
            except ValueError as e:
                print(e)
        elif opcion == "5":
            id_usuario = int(input("ID del usuario: "))
            isbn = input("ISBN del libro: ")
            try:
                prestamo = gp.realizar_prestamo(gl, gu, id_usuario, isbn)
                print(f"Préstamo realizado: {prestamo}")
            except ValueError as e:
                print(e)

        elif opcion == "6":
            id_usuario = int(input("ID del usuario: "))
            isbn = input("ISBN del libro: ")
            try:
                multa = gp.devolver_libro(gu, id_usuario, isbn)
                if multa is not None:
                    print(f"Libro devuelto con multa de {multa:.2f} € por retraso.")
                    notificador.enviar_notificacion(
                        f"Devolución con multa para '{isbn}'",
                        f"El usuario {id_usuario} devolvió el libro con ISBN '{isbn}' con una multa de {multa:.2f} €."
                    )
                else:
                    print("Libro devuelto a tiempo.")
                    notificador.enviar_notificacion(
                        f"Devolución realizada para '{isbn}'",
                        f"El usuario {id_usuario} ha devuelto el libro con ISBN '{isbn}'."
                    )
            except ValueError as e:
                print(e)
        elif opcion == "7":
            buscar_libro_por_isbn(gl)
        elif opcion == "8":
            libros = gl.listar_libros()
            print("\nLibros disponibles:")
            for libro in libros:
                print(f"- {libro.titulo} por {libro.autor} con ISBN {libro.isbn}")
        elif opcion == "9":
            prestamos_activos = gp.listar_prestamos()
            print("\nPréstamos activos:")
            for prestamo in prestamos_activos:
                print(f"- Usuario ID: {prestamo.id_usuario}, ISBN: {prestamo.isbn}, Fecha: {prestamo.fecha_prestamo}")

        elif opcion == "10":
            mostrar_prestamos_caducados(gp)

        elif opcion == "11":
            mostrar_historico(gp)

        elif opcion == "12":
            gl.exportar_json("data/catalogo_importar.json")
            print("Catálogo exportado a data/catalogo_importar.json.")
        elif opcion == "13":
            gl.exportar_csv("data/catalogo_importar.csv")
            print("Catálogo exportado a data/catalogo_importar.csv.")

        elif opcion == "14":
            try:
                ruta = input("Ingrese la ruta del archivo JSON: ")
                gl.importar_json(ruta)
                print("Catálogo importado desde JSON.")
            except FileNotFoundError:
                print("Archivo no encontrado.")
            except ValueError as e:
                print(f"Error al importar: {e}")

        elif opcion == "15":
            try:
                ruta = input("Ingrese la ruta del archivo CSV: ")
                gl.importar_csv(ruta)
                print("Catálogo importado desde CSV.")
            except FileNotFoundError:
                print("Archivo no encontrado.")
            except ValueError as e:
                print(f"Error al importar: {e}")
        elif opcion == "16":
            gu.exportar_usuarios("data/usuarios.json")
            print("Usuarios exportados a data/usuarios.json.")
        elif opcion == "17":
            try:
                ruta = input("Ingrese la ruta del archivo JSON de usuarios: ")
                gu.importar_usuarios(ruta)
                print("Usuarios importados desde JSON.")
            except FileNotFoundError:
                print("Archivo no encontrado.")
            except ValueError as e:
                print(f"Error al importar usuarios: {e}")
        elif opcion == "18":
            gu.exportar_usuarios_csv("data/usuarios.csv")
            print("Usuarios exportados a data/usuarios.csv.")
        elif opcion == "19":
            try:
                ruta = input("Ingrese la ruta del archivo CSV de usuarios: ")
                gu.importar_usuarios_csv(ruta)
                print("Usuarios importados desde CSV.")
            except FileNotFoundError:
                print("Archivo no encontrado.")
            except ValueError as e:
                print(f"Error al importar usuarios CSV: {e}")
        elif opcion == "20":
            gp.exportar_historico("data/historico_prestamos.json")
            print("Histórico de préstamos exportado a data/historico_prestamos.json.")
        elif opcion == "21":
            try:
                ruta = input("Ingrese la ruta del archivo JSON de historico: ")
                gp.importar_historico(ruta)
                print("Histórico importado desde JSON.")
            except FileNotFoundError:
                print("Archivo no encontrado.")
            except ValueError as e:
                print(f"Error al importar historico: {e}")
        elif opcion == "22":
            gp.exportar_historico_csv("data/historico_prestamos.csv")
            print("Histórico de préstamos exportado a data/historico_prestamos.csv.")
        elif opcion == "23":
            try:
                ruta = input("Ingrese la ruta del archivo CSV de historico: ")
                gp.importar_historico_csv(ruta)
                print("Histórico importado desde CSV.")
            except FileNotFoundError:
                print("Archivo no encontrado.")
            except ValueError as e:
                print(f"Error al importar historico CSV: {e}")

        elif opcion == "0":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()