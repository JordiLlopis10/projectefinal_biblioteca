from __future__ import annotations
from dataclasses import dataclass, field
from typing import List

@dataclass
class Usuario:
    nombre: str
    id_usuario: int
    _historial: List[str] = field(default_factory=list, repr=False)

    def __str__(self) -> str:
        return f"{self.nombre} (ID: {self.id_usuario})"

    def registrar_evento(self, evento: str) -> None:
        self._historial.append(evento)

    def historial(self) -> List[str]:
        return list(self._historial)