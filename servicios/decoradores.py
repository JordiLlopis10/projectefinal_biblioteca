from functools import wraps

def requiere_campos(*campos):
    def decorador(funcion):
        @wraps(funcion)
        def envoltura(*args, **kwargs):
            for campo in campos:
                if campo not in kwargs:
                    raise ValueError(f"Falta el campo requerido: {campo}")
            return funcion(*args, **kwargs)
        return envoltura
    return decorador

def loguear_accion(funcion):
    @wraps(funcion)
    def envoltura(*args, **kwargs):
        resultado = funcion(*args, **kwargs)
        print(f"Acción: {funcion.__name__} - Argumentos: {args} {kwargs}")
        return resultado
    return envoltura