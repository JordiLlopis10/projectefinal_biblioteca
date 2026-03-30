# Este módulo contiene la clase Libro, que representa un libro en la biblioteca. La clase incluye atributos para el título, el autor y el ISBN del libro. También proporciona un método para representar el libro como una cadena de texto, facilitando su visualización en la aplicación.
from __future__ import annotations
from .simple_metaclase import SimpleValidationMeta

class Libro(metaclass=SimpleValidationMeta):
    """Entidad inmutable: titulo y autor identifican la obra."""
    _required_fields = ['titulo', 'autor', 'isbn']

    def __init__(self, titulo: str, autor: str, isbn: str):
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn

        # Validación automática
        self._validar_campos_basicos()

        # Hacer la instancia "frozen" manualmente
        self._frozen = True

    def __setattr__(self, name, value):
        if hasattr(self, '_frozen') and self._frozen:
            raise AttributeError(f"can't set attribute '{name}' on frozen instance")
        super().__setattr__(name, value)

    def __str__(self) -> str:
        """Retorna representación textual del libro con título, autor e ISBN."""
        return f"{self.titulo} - {self.autor} (ISBN: {self.isbn})"

    def __repr__(self) -> str:
        return f"Libro(titulo='{self.titulo}', autor='{self.autor}', isbn='{self.isbn}')"