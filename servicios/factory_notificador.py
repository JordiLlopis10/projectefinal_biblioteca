# He usado el patrón de diseño Factory para crear instancias de notificadores sin acoplar el código a clases específicas. Esto permite una mayor flexibilidad y escalabilidad en el sistema de notificaciones.
from abc import ABC, abstractmethod

class Notificador(ABC):
    @abstractmethod
    def enviar_notificacion(self, mensaje: str, destinatario: str) -> None:
        pass

class NotificadorEmail(Notificador):
    def enviar_notificacion(self, mensaje: str, destinatario: str) -> None:
        print(f"Enviando email a {destinatario}: {mensaje}")

class NotificadorSMS(Notificador):
    def enviar_notificacion(self, mensaje: str, destinatario: str) -> None:
        print(f"Enviando SMS a {destinatario}: {mensaje}")

def crear_notificador(tipo: str) -> Notificador:
    if tipo == 'email':
        return NotificadorEmail()
    elif tipo == 'sms':
        return NotificadorSMS()
    else:
        raise ValueError(f"Tipo de notificador desconocido: {tipo}")