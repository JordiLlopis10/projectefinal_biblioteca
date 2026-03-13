from __future__ import annotations
from datetime import date
from modelos.prestamo import Prestamo
from servicios.gestion_libros import GestionLibros
from servicios.decoradores import loggear_accion


class GestionPrestamos:

    def __init__(self):
        self.prestamos: list[Prestamo] = []

    @loggear_accion
    def realizar_prestamo(self, gl: GestionLibros, id_usuario: int, titulo_libro: str) -> Prestamo:

        # comprobar que el libro existe en el catálogo
        libro_existe = False
        for libro in gl.listar_libros():
            if libro.titulo == titulo_libro:
                libro_existe = True
                break

        if not libro_existe:
            raise ValueError(f"El libro '{titulo_libro}' no existe.")

        # comprobar si ya está prestado
        hoy = date.today()
        for prestamo in self.prestamos:
            if prestamo.titulo_libro == titulo_libro and not prestamo.caducado(hoy):
                raise ValueError(f"El libro '{titulo_libro}' ya está prestado.")

        nuevo_prestamo = Prestamo(
            id_usuario=id_usuario,
            titulo_libro=titulo_libro,
            fecha_prestamo=date.today()
        )

        self.prestamos.append(nuevo_prestamo)
        return nuevo_prestamo


    def listar_prestamos(self) -> list[Prestamo]:
        return self.prestamos


    def prestamos_caducados(self, hoy: date) -> list[Prestamo]:
        return [prestamo for prestamo in self.prestamos if prestamo.caducado(hoy)]


    @loggear_accion
    def devolver_libro(self, id_usuario: int, titulo_libro: str) -> None:

        for prestamo in self.prestamos:
            if prestamo.id_usuario == id_usuario and prestamo.titulo_libro == titulo_libro:
                self.prestamos.remove(prestamo)
                return

        raise ValueError(
            f"No se encontró el préstamo del libro '{titulo_libro}' para el usuario {id_usuario}."
        )