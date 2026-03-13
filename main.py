from servicios.gestion_libros import GestionLibros
from servicios.gestion_usuarios import GestionUsuarios  
from servicios.gestion_prestamos import GestionPrestamos
from servicios.factory_notificador import crear_notificador

def menu():
    print("\n--- Biblioteca Digital ---")
    print("1.Añadir libro")
    print("2.Añadir usuario")
    print("3.Realizar préstamo")
    print("4.Devolver libro")
    print("5.Listar libros")
    print("6.Exportar catalogo JSON")
    print("7.Exportar catalogo CSV")
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
            gu.agregar_usuario(nombre, id_usuario)
            print(f"Usuario '{nombre}' añadido.")
        
        elif opcion == "3":
            id_usuario = int(input("ID del usuario: "))
            titulo_libro = input("Título del libro: ")
            try:
                prestamo = gp.realizar_prestamo(gl, id_usuario, titulo_libro)
                print(f"Préstamo realizado: {prestamo}")
            except ValueError as e:
                print(e)
        
        elif opcion == "4":
            id_usuario = int(input("ID del usuario: "))
            titulo_libro = input("Título del libro: ")
            gp.devolver_libro(id_usuario, titulo_libro)
            notificador.enviar_notificacion(f"Devolución realizada para '{titulo_libro}'", f"El usuario {id_usuario} ha devuelto el libro '{titulo_libro}'.")

        elif opcion == "5":
            libros = gl.listar_libros()
            print("\nLibros disponibles:")
            for libro in libros:
                print(f"- {libro.titulo} por {libro.autor}")
            
        elif opcion == "6":
            gl.exportar_json("catalogo.json")
            print("Catálogo exportado a catalogo.json.")
        elif opcion == "7":
            gl.exportar_csv("catalogo.csv")
            print("Catálogo exportado a catalogo.csv.")
            
        elif opcion == "0":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()