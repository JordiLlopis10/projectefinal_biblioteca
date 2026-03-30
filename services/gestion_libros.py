# Este módulo contiene la clase GestionLibros, que se encarga de gestionar las operaciones relacionadas con los libros de la biblioteca, como agregar, eliminar, buscar y listar libros. También incluye funcionalidades para exportar e importar datos de libros en formatos JSON y CSV.
from __future__ import annotations
from models.libro import Libro
from typing import Iterable
from services.mixins import ExportarMixin, ImportarMixins
from services.decoradores import loggear_accion, requiere_campos

class GestionLibros(ExportarMixin, ImportarMixins):
    def __init__(self):
        """Inicializa el gestor de libros con diccionario vacío."""
        self.libros: dict[str, Libro] = {}

    @loggear_accion
    @requiere_campos('titulo', 'autor', 'isbn')
    def agregar_libro(self, titulo: str, autor: str, isbn: str) -> Libro:
        """Añade un nuevo libro al catálogo. Levanta error si ISBN ya existe."""
        if isbn in self.libros:
            raise ValueError(f"El libro con ISBN {isbn} ya existe")
        nuevo_libro = Libro(titulo=titulo, autor=autor, isbn=isbn)
        self.libros[isbn] = nuevo_libro
        return nuevo_libro
    
    @loggear_accion
    def baja_libro(self, isbn: str) -> None:
        """Elimina un libro del catálogo por ISBN."""
        if isbn not in self.libros:
            raise ValueError(f"No se encontró el libro con ISBN {isbn}.")
        del self.libros[isbn]
    
    def buscar_libro(self, isbn: str) -> Libro:
        """Busca y retorna un libro por su ISBN."""
        if isbn not in self.libros:
            raise ValueError(f"No se encontró el libro con ISBN {isbn}.")
        return self.libros[isbn]
    
    def listar_libros(self) -> Iterable[Libro]:
        """Retorna todos los libros del catálogo."""
        return self.libros.values()
    
    def exportar_json(self, ruta):
        """Exporta el catálogo a archivo JSON."""
        return super().exportar_json(ruta)
    
    def exportar_csv(self, ruta):
        """Exporta el catálogo a archivo CSV."""
        return super().exportar_csv(ruta)
    
    def importar_json(self, ruta):
        """Importa libros desde archivo JSON."""
        return super().importar_json(ruta)
    
    def importar_csv(self, ruta):
        """Importa libros desde archivo CSV."""
        return super().importar_csv(ruta)
    