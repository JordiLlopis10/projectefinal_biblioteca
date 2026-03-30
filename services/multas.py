#Patron de diseño Singleton para gestionar multas de usuarios por retrasos en devoluciones, porque solo necesitamos una instancia de este servicio para mantener un registro centralizado de todas las multas asignadas a los usuarios. Esto asegura que la información sobre las multas sea consistente y fácilmente accesible desde cualquier parte de la aplicación.
from __future__ import annotations
from datetime import date

class MultaService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        """Implementa patrón Singleton: retorna siempre la misma instancia."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Inicializa el diccionario de multas solo la primera vez."""
        if not hasattr(self, 'multas'):
            self.multas: dict[int, list[dict]] = {}

    def asignar_multa(self, id_usuario: int, isbn: str, dias_retraso: int, tasa: float = 1.0) -> float:
        """Calcula y registra una multa por retraso en devolución."""
        monto = round(dias_retraso * tasa, 2)
        registro = {
            'fecha': date.today().isoformat(),
            'isbn': isbn,
            'dias_retraso': dias_retraso,
            'monto': monto,
        }
        self.multas.setdefault(id_usuario, []).append(registro)
        return monto

    def obtener_multas(self, id_usuario: int | None = None):
        """Obtiene multas de un usuario específico o todas si no se especifica usuario."""
        if id_usuario is None:
            return self.multas
        return self.multas.get(id_usuario, [])
