# Guía de Usuario - Sistema de Gestión de Biblioteca

## Introducción

Este es un sistema de gestión completo para bibliotecas que permite administrar libros, usuarios y préstamos. El sistema incluye funcionalidades de importación/exportación de datos y cálculo automático de multas por retrasos.

## Requisitos

- Python 3.13 o superior
- Todas las dependencias están incluidas en el código estándar de Python

## Cómo ejecutar

1. Abre una terminal en el directorio del proyecto
2. Ejecuta: `python main.py`
3. Selecciona la opción deseada del menú

## Funcionalidades del Sistema

### Gestión de Libros

**1. Añadir libro**
- Permite agregar nuevos libros al catálogo
- Requiere: Título, Autor, ISBN

**6. Buscar libro por ISBN**
- Busca un libro específico usando su ISBN
- Muestra toda la información del libro

**7. Listar libros**
- Muestra todos los libros disponibles en el catálogo

### Gestión de Usuarios

**2. Añadir usuario**
- Registra nuevos usuarios en el sistema
- Requiere: Nombre, ID de usuario único

**3. Listar usuarios**
- Muestra todos los usuarios registrados

### Gestión de Préstamos

**4. Realizar préstamo**
- Presta un libro a un usuario
- Requiere: ID de usuario, ISBN del libro
- Verifica que el libro esté disponible
- Establece un plazo de 14 días

**5. Devolver libro**
- Registra la devolución de un libro
- Calcula automáticamente multas por retraso (1.5€ por día)
- Mueve el préstamo al histórico

**8. Listar préstamos activos**
- Muestra todos los préstamos que aún no han sido devueltos

**9. Listar préstamos caducados no devueltos**
- Muestra préstamos vencidos que requieren atención
- Incluye días de retraso

**10. Listar histórico de préstamos**
- Muestra todos los préstamos completados
- Incluye información de multas si aplica

### Importación/Exportación de Datos

**Exportar datos:**
- 11. Exportar catálogo a JSON
- 12. Exportar catálogo a CSV
- 15. Exportar usuarios a JSON
- 17. Exportar usuarios a CSV
- 19. Exportar histórico de préstamos a JSON
- 21. Exportar histórico de préstamos a CSV

Los archivos se guardan automáticamente en la carpeta `data/`

**Importar datos:**
- 13. Importar catálogo desde JSON
- 14. Importar catálogo desde CSV
- 16. Importar usuarios desde JSON
- 18. Importar usuarios desde CSV
- 20. Importar histórico desde JSON
- 22. Importar histórico desde CSV

Para importar, ingresa la ruta completa del archivo cuando se solicite.

## Archivos de Datos

- `data/catalogo_importar.json/csv`: Catálogo de libros
- `data/usuarios.json/csv`: Lista de usuarios
- `data/historico_prestamos.json/csv`: Histórico de préstamos

## Reglas del Sistema

- **ISBN único**: Cada libro debe tener un ISBN único
- **ID usuario único**: Cada usuario debe tener un ID único
- **Préstamos**: Un libro no puede prestarse si ya está prestado
- **Plazo**: Los préstamos tienen un plazo máximo de 14 días
- **Multas**: 1.5€ por cada día de retraso
- **Devoluciones**: Solo se pueden devolver libros que estén prestados


- El sistema calcula automáticamente las fechas de vencimiento
- Las multas se calculan al momento de la devolución
- Todos los datos se persisten en archivos JSON/CSV
- El sistema incluye validaciones para evitar errores comunes
- Las importaciones pueden fallar si los archivos no tienen el formato correcto

## Soporte

Si encuentras errores o necesitas ayuda, revisa:
1. Que los archivos de datos existan en la carpeta `data/`
2. Que los ISBN e IDs sean únicos
3. Que los libros a prestar estén disponibles
4. Que los archivos de importación tengan el formato correcto