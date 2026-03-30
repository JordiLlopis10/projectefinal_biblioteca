# Este módulo contiene la clase Usuario, que representa a un usuario de la biblioteca. La clase incluye atributos para el nombre del usuario, su ID y un historial de eventos relacionados con sus interacciones con la biblioteca. También proporciona métodos para registrar eventos y obtener el historial completo de interacciones.
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List

@dataclass
class Usuario:
    nombre: str
    id_usuario: int
    _historial: List[str] = field(default_factory=list, repr=False)

    def __str__(self) -> str:
        """Retorna representación textual del usuario."""
        return f"{self.nombre} (ID: {self.id_usuario})"

    def registrar_evento(self, evento: str) -> None:
        """Añade un evento al historial del usuario."""
        self._historial.append(evento)

    def historial(self) -> List[str]:
        """Retorna copia del historial de eventos del usuario."""
        return list(self._historial)