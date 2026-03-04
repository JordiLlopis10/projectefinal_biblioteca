from __future__ import annotations
from datetime import date
from modelos.prestamo import Prestamo
from modelos.libro import Libro
from servicios.decoradores import loggear_accion

class GestionPrestamos:
    def __init__(self):
        self.prestamos: list[Prestamo] = []

    @loggear_accion
    def realizar_prestamo(self, id_usuario: int, titulo_libro: str) -> Prestamo:
        nuevo_prestamo = Prestamo(id_usuario=id_usuario, titulo_libro=titulo_libro, fecha_prestamo=date.today().isoformat())
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
        raise ValueError(f"No se encontró el préstamo para el usuario {id_usuario} y el libro '{titulo_libro}'.")