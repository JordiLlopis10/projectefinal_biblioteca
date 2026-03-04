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