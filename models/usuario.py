# Este módulo contiene la clase Usuario, que representa a un usuario de la biblioteca. La clase incluye atributos para el nombre del usuario, su ID y un historial de eventos relacionados con sus interacciones con la biblioteca. También proporciona métodos para registrar eventos y obtener el historial completo de interacciones.
from __future__ import annotations
from typing import List
from .simple_metaclase import SimpleValidationMeta

class Usuario(metaclass=SimpleValidationMeta):
    _required_fields = ['nombre', 'id_usuario']

    def __init__(self, nombre: str, id_usuario: int):
        self.nombre = nombre
        self.id_usuario = id_usuario
        self._historial: List[str] = []

        # Validación automática
        self._validar_campos_basicos()

    def __str__(self) -> str:
        """Retorna representación textual del usuario."""
        return f"{self.nombre} (ID: {self.id_usuario})"

    def registrar_evento(self, evento: str) -> None:
        """Añade un evento al historial del usuario."""
        self._historial.append(evento)

    def historial(self) -> List[str]:
        """Retorna copia del historial de eventos del usuario."""
        return list(self._historial)