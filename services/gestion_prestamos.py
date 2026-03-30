# Este módulo contiene la clase GestionPrestamos, que se encarga de gestionar las operaciones relacionadas con los préstamos de libros en la biblioteca, como realizar préstamos, devolver libros y listar préstamos activos y caducados. También incluye funcionalidades para exportar e importar el histórico de préstamos en formatos JSON y CSV.
from __future__ import annotations
from datetime import date
from models.prestamo import Prestamo
from services.gestion_libros import GestionLibros
from services.gestion_usuarios import GestionUsuarios
from services.decoradores import loggear_accion
from services.mixins import ExportarMixin, ImportarMixins
from services.multas import MultaService


class GestionPrestamos(ExportarMixin, ImportarMixins):

    def __init__(self):
        """Inicializa gestor de préstamos con listas vacías de préstamos activos e histórico."""
        self.prestamos: list[Prestamo] = []
        self.historico: list[Prestamo] = []
        self.multa_service = MultaService()

    @loggear_accion
    def realizar_prestamo(self, gl: GestionLibros, gu: GestionUsuarios, id_usuario: int, isbn: str) -> Prestamo:
        """Registra un nuevo préstamo. Verifica que libro existe y no está prestado."""

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
        
        # Registrar evento en el historial del usuario
        usuario = gu.obtener_usuario(id_usuario)
        usuario.registrar_evento(f"Préstamo realizado: ISBN '{isbn}' - {date.today()}")
        
        return nuevo_prestamo


    def listar_prestamos(self) -> list[Prestamo]:
        """Retorna lista de todos los préstamos activos."""
        return self.prestamos


    def prestamos_caducados_no_devueltos(self, hoy: date) -> list[Prestamo]:
        """Retorna préstamos vencidos que aún no han sido devueltos."""
        return [prestamo for prestamo in self.prestamos if prestamo.caducado(hoy)]


    def listar_historico(self) -> list[Prestamo]:
        """Retorna lista de todos los préstamos completados."""
        return self.historico

    def exportar_historico(self, ruta):
        """Exporta histórico de préstamos a archivo JSON."""
        return super().exportar_historico(ruta)

    def importar_historico(self, ruta):
        """Importa histórico de préstamos desde archivo JSON."""
        return super().importar_historico(ruta)

    @loggear_accion
    def devolver_libro(self, gu: GestionUsuarios, id_usuario: int, isbn: str) -> float | None:
        """Registra devolución de libro. Calcula multa si hay retraso. Retorna monto de multa o None."""
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
                    
                    # Registrar evento en el historial del usuario
                    usuario = gu.obtener_usuario(id_usuario)
                    usuario.registrar_evento(f"Devolución con retraso: ISBN '{isbn}' - Multa: {multa:.2f}€ - {hoy}")
                    
                    return multa

                prestamo.fecha_devolucion = hoy
                prestamo.multa = None
                self.historico.append(prestamo)
                self.prestamos.remove(prestamo)
                
                # Registrar evento en el historial del usuario
                usuario = gu.obtener_usuario(id_usuario)
                usuario.registrar_evento(f"Devolución a tiempo: ISBN '{isbn}' - {hoy}")
                
                return None

        raise ValueError(
            f"No se encontró el préstamo del libro con ISBN '{isbn}' para el usuario {id_usuario}."
        )