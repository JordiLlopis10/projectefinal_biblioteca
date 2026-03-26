from datetime import date
from servicios.gestion_prestamos import GestionPrestamos
from servicios.gestion_libros import GestionLibros

def buscar_libro_por_isbn(gl: GestionLibros) -> None:
    isbn = input("Ingrese el ISBN del libro a buscar: ")
    try:
        libro = gl.buscar_libro(isbn)
        print(f"\nLibro encontrado:")
        print(f"- Título: {libro.titulo}")
        print(f"- Autor: {libro.autor}")
        print(f"- ISBN: {libro.isbn}")
    except ValueError as e:
        print(f"Error: {e}")

def mostrar_prestamos_caducados(gp: GestionPrestamos) -> None:
    hoy = date.today()
    prestamos_caducados = gp.prestamos_caducados_no_devueltos(hoy)
    print("\nPréstamos caducados no devueltos:")
    if prestamos_caducados:
        for prestamo in prestamos_caducados:
            dias_retraso = (hoy - prestamo.fecha_devolucion_esperada).days
            print(f"- Usuario ID: {prestamo.id_usuario}, ISBN: {prestamo.isbn}, Fecha préstamo: {prestamo.fecha_prestamo}, Días de retraso: {dias_retraso}")
    else:
        print("No hay préstamos caducados.")

def mostrar_historico(gp: GestionPrestamos) -> None:
    historico = gp.listar_historico()
    print("\nHistórico de préstamos:")
    if historico:
        for prestamo in historico:
            multa_str = f", Multa: {prestamo.multa:.2f} €" if prestamo.multa else ""
            print(f"- Usuario ID: {prestamo.id_usuario}, ISBN: {prestamo.isbn}, Prestado: {prestamo.fecha_prestamo}, Devuelto: {prestamo.fecha_devolucion}{multa_str}")
    else:
        print("No hay préstamos en el histórico.")