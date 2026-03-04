from dataclasses import dataclass
from datetime import date, timedelta


@dataclass
class Prestamo:
    id_usuario: int
    titulo_libro: str
    fecha_prestamo: date
    dias_plazo: int = 14

    @property
    def fecha_devolucion(self) -> date:
        return date.fromisoformat(self.fecha_prestamo) + timedelta(days=self.dias_plazo)
    
    def caducado(self,hoy: date) -> bool:
        return hoy > self.fecha_devolucion