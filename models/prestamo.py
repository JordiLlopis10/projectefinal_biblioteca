# Este módulo contiene la clase Prestamo, que representa un préstamo de un libro en la biblioteca. La clase incluye atributos para el ID del usuario, el ISBN del libro, la fecha del préstamo, el plazo de devolución, la fecha de devolución (si ya se ha devuelto) y la multa (si corresponde). También proporciona métodos para calcular la fecha de devolución esperada y verificar si el préstamo está caducado.
from datetime import date, timedelta
from typing import Optional
from .simple_metaclase import SimpleValidationMeta

class Prestamo(metaclass=SimpleValidationMeta):
    _required_fields = ['id_usuario', 'isbn']

    def __init__(self, id_usuario: int, isbn: str, fecha_prestamo: date,
                 dias_plazo: int = 14, fecha_devolucion: Optional[date] = None,
                 multa: Optional[float] = None):
        self.id_usuario = id_usuario
        self.isbn = isbn
        self.fecha_prestamo = fecha_prestamo
        self.dias_plazo = dias_plazo
        self.fecha_devolucion = fecha_devolucion
        self.multa = multa

        # Validación automática básica
        self._validar_campos_basicos()

        # Validaciones adicionales específicas
        self.__post_init__()

    def __post_init__(self):
        """Validaciones adicionales específicas del préstamo."""
        # Validaciones específicas adicionales
        if self.fecha_prestamo > date.today():
            raise ValueError("La fecha de préstamo no puede ser futura")

        if self.dias_plazo <= 0:
            raise ValueError("Los días de plazo deben ser positivos")

        if self.multa is not None and self.multa < 0:
            raise ValueError("La multa no puede ser negativa")

    @property
    def fecha_devolucion_esperada(self) -> date:
        """Calcula la fecha límite de devolución del préstamo."""
        return self.fecha_prestamo + timedelta(days=self.dias_plazo)

    def caducado(self, hoy: date) -> bool:
        """Verifica si el préstamo está vencido y aún no devuelto."""
        if self.fecha_devolucion:
            return False  # Ya devuelto
        return hoy > self.fecha_devolucion_esperada