from dataclasses import dataclass
from datetime import date, timedelta
from typing import Optional


@dataclass
class Prestamo:
    id_usuario: int
    isbn: str
    fecha_prestamo: date
    dias_plazo: int = 14
    fecha_devolucion: Optional[date] = None
    multa: Optional[float] = None

    @property
    def fecha_devolucion_esperada(self) -> date:
        return self.fecha_prestamo + timedelta(days=self.dias_plazo)

    def caducado(self, hoy: date) -> bool:
        if self.fecha_devolucion:
            return False  # Ya devuelto
        return hoy > self.fecha_devolucion_esperada