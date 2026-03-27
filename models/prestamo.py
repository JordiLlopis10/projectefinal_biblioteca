# Este módulo contiene la clase Prestamo, que representa un préstamo de un libro en la biblioteca. La clase incluye atributos para el ID del usuario, el ISBN del libro, la fecha del préstamo, el plazo de devolución, la fecha de devolución (si ya se ha devuelto) y la multa (si corresponde). También proporciona métodos para calcular la fecha de devolución esperada y verificar si el préstamo está caducado.
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