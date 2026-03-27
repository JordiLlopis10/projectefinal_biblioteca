# Tiene la responsabilidad de implementar el patrón Observer para notificar a los usuarios sobre eventos importantes, como la devolución de un libro o la disponibilidad de un nuevo título.
class Sujeto:
    def __init__(self):
        self._observadores = []

    def agregar_observador(self, observador):
        self._observadores.append(observador)

    def eliminar_observador(self, observador):
        self._observadores.remove(observador)

    def notificar_observadores(self, mensaje):
        for observador in self._observadores:
            observador.actualizar(mensaje)

class Observador:
    def actualizar(self, mensaje):
        raise NotImplementedError("Subclase debe implementar el método actualizar")