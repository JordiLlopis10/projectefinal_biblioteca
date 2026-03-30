# Metaclase simple para validación básica automática
# Esta metaclase valida automáticamente campos básicos en las clases que la usan

class SimpleValidationMeta(type):
    """
    Metaclase simple que valida campos básicos automáticamente.

    Validaciones básicas:
    - Campos requeridos no pueden estar vacíos (strings) o ser <= 0 (números)
    """

    def __new__(cls, name: str, bases: tuple, namespace: dict, **kwargs):
        """Crea la clase con validación automática básica."""
        # Crear la clase normalmente
        new_class = super().__new__(cls, name, bases, namespace)

        # Definir campos que requieren validación básica
        required_fields = getattr(new_class, '_required_fields', [])

        # Agregar método de validación a la clase
        def _validar_campos_basicos(self):
            """Valida campos requeridos básicos."""
            for field_name in required_fields:
                if hasattr(self, field_name):
                    value = getattr(self, field_name)
                    if isinstance(value, str) and not value.strip():
                        raise ValueError(f"El campo '{field_name}' no puede estar vacío")
                    elif isinstance(value, (int, float)) and value <= 0:
                        raise ValueError(f"El campo '{field_name}' debe ser mayor que 0")

        # Agregar el método a la clase
        new_class._validar_campos_basicos = _validar_campos_basicos

        return new_class