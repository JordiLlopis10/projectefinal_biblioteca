from servicios.gestion_libros import GestionLibros
from servicios.gestion_usuarios import GestionUsuarios  
from servicios.gestion_prestamos import GestionPrestamos
from servicios.factory_notificador import crear_notificador
from servicios.listar import buscar_libro_por_isbn, mostrar_prestamos_caducados, mostrar_historico

def menu():
    print("\n--- Biblioteca Digital ---")
    print("1.Añadir libro")
    print("2.Añadir usuario")
    print("3.Listar usuarios")
    print("4.Realizar préstamo")
    print("5.Devolver libro")
    print("6.Buscar libro por ISBN")
    print("7.Listar libros")
    print("8.Listar préstamos activos")
    print("9.Listar préstamos caducados no devueltos")
    print("10.Listar histórico de préstamos")
    print("11.Exportar catalogo JSON")
    print("12.Exportar catalogo CSV")
    print("13.Importar catalogo JSON")
    print("14.Importar catalogo CSV")
    print("15.Exportar usuarios JSON")
    print("16.Importar usuarios JSON")
    print("17.Exportar usuarios CSV")
    print("18.Importar usuarios CSV")
    print("19.Exportar historico de prestamos JSON")
    print("20.Importar historico de prestamos JSON")
    print("21.Exportar historico de prestamos CSV")
    print("22.Importar historico de prestamos CSV")
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
            isbn = input("ISBN del libro: ")
            try:
                prestamo = gp.realizar_prestamo(gl, id_usuario, isbn)
                print(f"Préstamo realizado: {prestamo}")
            except ValueError as e:
                print(e)

        elif opcion == "5":
            id_usuario = int(input("ID del usuario: "))
            isbn = input("ISBN del libro: ")
            try:
                multa = gp.devolver_libro(id_usuario, isbn)
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
        elif opcion == "6":
            buscar_libro_por_isbn(gl)
        elif opcion == "7":
            libros = gl.listar_libros()
            print("\nLibros disponibles:")
            for libro in libros:
                print(f"- {libro.titulo} por {libro.autor} con ISBN {libro.isbn}")
        elif opcion == "8":
            prestamos_activos = gp.listar_prestamos()
            print("\nPréstamos activos:")
            for prestamo in prestamos_activos:
                print(f"- Usuario ID: {prestamo.id_usuario}, ISBN: {prestamo.isbn}, Fecha: {prestamo.fecha_prestamo}")

        elif opcion == "9":
            mostrar_prestamos_caducados(gp)

        elif opcion == "10":
            mostrar_historico(gp)

        elif opcion == "11":
            gl.exportar_json("catalogo_importar.json")
            print("Catálogo exportado a catalogo_importar.json.")
        elif opcion == "12":
            gl.exportar_csv("catalogo_importar.csv")
            print("Catálogo exportado a catalogo_importar.csv.")

        elif opcion == "13":
            try:
                ruta = input("Ingrese la ruta del archivo JSON: ")
                gl.importar_json(ruta)
                print("Catálogo importado desde JSON.")
            except FileNotFoundError:
                print("Archivo no encontrado.")
            except ValueError as e:
                print(f"Error al importar: {e}")

        elif opcion == "14":
            try:
                ruta = input("Ingrese la ruta del archivo CSV: ")
                gl.importar_csv(ruta)
                print("Catálogo importado desde CSV.")
            except FileNotFoundError:
                print("Archivo no encontrado.")
            except ValueError as e:
                print(f"Error al importar: {e}")
        elif opcion == "15":
            gu.exportar_usuarios("usuarios.json")
            print("Usuarios exportados a usuarios.json.")
        elif opcion == "16":
            try:
                ruta = input("Ingrese la ruta del archivo JSON de usuarios: ")
                gu.importar_usuarios(ruta)
                print("Usuarios importados desde JSON.")
            except FileNotFoundError:
                print("Archivo no encontrado.")
            except ValueError as e:
                print(f"Error al importar usuarios: {e}")
        elif opcion == "17":
            gu.exportar_usuarios_csv("usuarios.csv")
            print("Usuarios exportados a usuarios.csv.")
        elif opcion == "18":
            try:
                ruta = input("Ingrese la ruta del archivo CSV de usuarios: ")
                gu.importar_usuarios_csv(ruta)
                print("Usuarios importados desde CSV.")
            except FileNotFoundError:
                print("Archivo no encontrado.")
            except ValueError as e:
                print(f"Error al importar usuarios CSV: {e}")
        elif opcion == "19":
            gp.exportar_historico("historico_prestamos.json")
            print("Histórico de préstamos exportado a historico_prestamos.json.")
        elif opcion == "20":
            try:
                ruta = input("Ingrese la ruta del archivo JSON de historico: ")
                gp.importar_historico(ruta)
                print("Histórico importado desde JSON.")
            except FileNotFoundError:
                print("Archivo no encontrado.")
            except ValueError as e:
                print(f"Error al importar historico: {e}")
        elif opcion == "21":
            gp.exportar_historico_csv("historico_prestamos.csv")
            print("Histórico de préstamos exportado a historico_prestamos.csv.")
        elif opcion == "22":
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