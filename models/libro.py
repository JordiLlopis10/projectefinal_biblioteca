# Este módulo contiene la clase Libro, que representa un libro en la biblioteca. La clase incluye atributos para el título, el autor y el ISBN del libro. También proporciona un método para representar el libro como una cadena de texto, facilitando su visualización en la aplicación.
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Libro:
    """Entidad inmutable: titulo y autor identifican la obra."""
    titulo: str
    autor: str
    isbn: str

    def __str__(self) -> str:
        return f"{self.titulo} - {self.autor} (ISBN: {self.isbn})"