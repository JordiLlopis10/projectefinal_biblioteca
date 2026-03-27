from __future__ import annotations
from datetime import date
from modelos.prestamo import Prestamo
from servicios.gestion_libros import GestionLibros
from servicios.decoradores import loggear_accion
from servicios.mixins import ExportarMixin, ImportarMixins
from servicios.multas import MultaService


class GestionPrestamos(ExportarMixin, ImportarMixins):

    def __init__(self):
        self.prestamos: list[Prestamo] = []
        self.historico: list[Prestamo] = []
        self.multa_service = MultaService()

    @loggear_accion
    def realizar_prestamo(self, gl: GestionLibros, id_usuario: int, isbn: str) -> Prestamo:

        # comprobar que el libro existe en el catálogo
        libro_existe = False
        for libro in gl.listar_libros():
            if libro.isbn == isbn:
                libro_existe = True
                break

        if not libro_existe:
            raise ValueError(f"El libro con ISBN '{isbn}' no existe.")

        # comprobar si ya está prestado
        for prestamo in self.prestamos:
            if prestamo.isbn == isbn:
                raise ValueError(f"El libro con ISBN '{isbn}' ya está prestado.")

        nuevo_prestamo = Prestamo(
            id_usuario=id_usuario,
            isbn=isbn,
            fecha_prestamo=date.today()
        )

        self.prestamos.append(nuevo_prestamo)
        return nuevo_prestamo


    def listar_prestamos(self) -> list[Prestamo]:
        return self.prestamos


    def prestamos_caducados_no_devueltos(self, hoy: date) -> list[Prestamo]:
        return [prestamo for prestamo in self.prestamos if prestamo.caducado(hoy)]


    def listar_historico(self) -> list[Prestamo]:
        return self.historico

    def exportar_historico(self, ruta):
        return super().exportar_historico(ruta)

    def importar_historico(self, ruta):
        return super().importar_historico(ruta)

    @loggear_accion
    def devolver_libro(self, id_usuario: int, isbn: str) -> float | None:
        hoy = date.today()

        for prestamo in self.prestamos:
            if prestamo.id_usuario == id_usuario and prestamo.isbn == isbn:
                caducado = prestamo.caducado(hoy)

                if caducado:
                    dias_retraso = (hoy - prestamo.fecha_devolucion_esperada).days
                    dias_retraso = max(dias_retraso, 0)
                    multa = self.multa_service.asignar_multa(id_usuario, isbn, dias_retraso, tasa=1.5)
                    prestamo.fecha_devolucion = hoy
                    prestamo.multa = multa
                    self.historico.append(prestamo)
                    self.prestamos.remove(prestamo)
                    return multa

                prestamo.fecha_devolucion = hoy
                prestamo.multa = None
                self.historico.append(prestamo)
                self.prestamos.remove(prestamo)
                return None

        raise ValueError(
            f"No se encontró el préstamo del libro con ISBN '{isbn}' para el usuario {id_usuario}."
        )