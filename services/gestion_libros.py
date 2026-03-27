# Este módulo contiene la clase GestionLibros, que se encarga de gestionar las operaciones relacionadas con los libros de la biblioteca, como agregar, eliminar, buscar y listar libros. También incluye funcionalidades para exportar e importar datos de libros en formatos JSON y CSV.
from __future__ import annotations
from models.libro import Libro
from typing import Iterable
from services.mixins import ExportarMixin, ImportarMixins
from services.decoradores import loggear_accion, requiere_campos

class GestionLibros(ExportarMixin, ImportarMixins):
    def __init__(self):
        self.libros: dict[str, Libro] = {}

    @loggear_accion
    @requiere_campos('titulo', 'autor', 'isbn')
    def agregar_libro(self, titulo: str, autor: str, isbn: str) -> Libro:
        if isbn in self.libros:
            raise ValueError(f"El libro con ISBN {isbn} ya existe")
        nuevo_libro = Libro(titulo=titulo, autor=autor, isbn=isbn)
        self.libros[isbn] = nuevo_libro
        return nuevo_libro
    
    @loggear_accion
    def baja_libro(self, isbn: str) -> None:
        if isbn not in self.libros:
            raise ValueError(f"No se encontró el libro con ISBN {isbn}.")
        del self.libros[isbn]
    
    def buscar_libro(self, isbn: str) -> Libro:
        if isbn not in self.libros:
            raise ValueError(f"No se encontró el libro con ISBN {isbn}.")
        return self.libros[isbn]
    
    def listar_libros(self) -> Iterable[Libro]:
        return self.libros.values()
    
    def exportar_json(self, ruta):
        return super().exportar_json(ruta)
    
    def exportar_csv(self, ruta):
        return super().exportar_csv(ruta)
    
    def importar_json(self, ruta):
        return super().importar_json(ruta)
    
    def importar_csv(self, ruta):
        return super().importar_csv(ruta)
    