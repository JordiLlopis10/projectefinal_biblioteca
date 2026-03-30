# He usado el patrón de diseño Factory para crear instancias de notificadores sin acoplar el código a clases específicas. Esto permite una mayor flexibilidad y escalabilidad en el sistema de notificaciones.
from abc import ABC, abstractmethod

class Notificador(ABC):
    """Clase abstracta que define la interfaz para notificadores."""
    @abstractmethod
    def enviar_notificacion(self, mensaje: str, destinatario: str) -> None:
        """Envía una notificación al destinatario especificado."""
        pass

class NotificadorEmail(Notificador):
    """Implementación de notificador que envía emails."""
    def enviar_notificacion(self, mensaje: str, destinatario: str) -> None:
        """Simula el envío de un email."""
        print(f"Enviando email a {destinatario}: {mensaje}")

class NotificadorSMS(Notificador):
    """Implementación de notificador que envía SMS."""
    def enviar_notificacion(self, mensaje: str, destinatario: str) -> None:
        """Simula el envío de un SMS."""
        print(f"Enviando SMS a {destinatario}: {mensaje}")

def crear_notificador(tipo: str) -> Notificador:
    """Factory: crea instancia de notificador según tipo especificado."""
    if tipo == 'email':
        return NotificadorEmail()
    elif tipo == 'sms':
        return NotificadorSMS()
    else:
        raise ValueError(f"Tipo de notificador desconocido: {tipo}")