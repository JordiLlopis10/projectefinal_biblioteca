#!/usr/bin/env python3
"""
Demostración de la metaclase SimpleValidationMeta

Esta metaclase es más sencilla pero válida para validaciones básicas.
"""

from models.libro import Libro
from models.usuario import Usuario
from models.prestamo import Prestamo
from datetime import date

def demo_metaclase_simple():
    """Demuestra la metaclase simple en funcionamiento."""
    print("DEMOSTRACIÓN DE LA METACLASE SimpleValidationMeta")
    print("=" * 60)

    print("\n=== Creaciones Exitosas ===")

    # Libro válido
    try:
        libro = Libro(titulo="El Quijote", autor="Cervantes", isbn="1234567890")
        print(f"✓ Libro creado: {libro}")
    except Exception as e:
        print(f"✗ Error: {e}")

    # Usuario válido
    try:
        usuario = Usuario(nombre="María García", id_usuario=1)
        print(f"✓ Usuario creado: {usuario}")
    except Exception as e:
        print(f"✗ Error: {e}")

    # Préstamo válido
    try:
        hoy = date.today()
        prestamo = Prestamo(id_usuario=1, isbn="1234567890", fecha_prestamo=hoy)
        print(f"✓ Préstamo creado: Usuario {prestamo.id_usuario}, ISBN {prestamo.isbn}")
    except Exception as e:
        print(f"✗ Error: {e}")

    print("\n=== Validaciones que Fallan ===")

    # Libro con título vacío
    try:
        libro = Libro(titulo="", autor="Cervantes", isbn="1234567890")
        print(f"✗ Libro creado inesperadamente: {libro}")
    except ValueError as e:
        print(f"✓ Validación correcta: {e}")

    # Usuario con ID negativo
    try:
        usuario = Usuario(nombre="Usuario", id_usuario=-1)
        print(f"✗ Usuario creado inesperadamente: {usuario}")
    except ValueError as e:
        print(f"✓ Validación correcta: {e}")

    # Préstamo con fecha futura
    try:
        futuro = date.today().replace(year=date.today().year + 1)
        prestamo = Prestamo(id_usuario=1, isbn="1234567890", fecha_prestamo=futuro)
        print(f"✗ Préstamo creado inesperadamente: {prestamo}")
    except ValueError as e:
        print(f"✓ Validación correcta: {e}")

    print("\n" + "=" * 60)
    print("✅ Demostración completada!")
    print("\nLa metaclase SimpleValidationMeta valida:")
    print("- ✅ Campos requeridos no vacíos")
    print("- ✅ Números mayores que 0")
    print("- ✅ Y permite validaciones adicionales en __post_init__")

if __name__ == "__main__":
    demo_metaclase_simple()