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