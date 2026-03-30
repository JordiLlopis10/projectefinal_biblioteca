# Este módulo contiene decoradores para validar la presencia de campos requeridos en las funciones y para loggear las acciones realizadas en la aplicación, facilitando la depuración y el seguimiento de las operaciones.
import inspect
from functools import wraps


def requiere_campos(*campos):
    """Decorador que valida que los campos especificados no estén vacíos."""
    def decorador(funcion):

        @wraps(funcion)
        def envoltura(*args, **kwargs):

            sig = inspect.signature(funcion)
            valores = sig.bind(*args, **kwargs)
            valores.apply_defaults()

            for campo in campos:
                if not valores.arguments.get(campo):
                    raise ValueError(f"Falta el campo requerido: {campo}")

            return funcion(*args, **kwargs)

        return envoltura
    return decorador

def loggear_accion(funcion):
    """Decorador que registra (loggea) la ejecución de una función con sus argumentos."""
    @wraps(funcion)
    def envoltura(*args, **kwargs):
        resultado = funcion(*args, **kwargs)
        print(f"Acción: {funcion.__name__} - Argumentos: {args} {kwargs}")
        return resultado
    return envoltura