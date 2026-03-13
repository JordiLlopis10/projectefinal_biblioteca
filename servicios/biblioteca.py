# #Aqui quiero comprobar que no se preste un libro que no existe, que no se preste un libro que ya esta prestado, y que no se pueda devolver un libro que no se ha prestado. saber si un prestamo esta activo o no, el historico de prestamos, y los prestamos caducados. Tambien quiero que se envie una notificacion cada vez que se realice un prestamo o una devolucion.

# from datetime import date
# from servicios.gestion_libros import GestionLibros
# from servicios.gestion_usuarios import GestionUsuarios
# from servicios.gestion_prestamos import GestionPrestamos
# from servicios.factory_notificador import crear_notificador


# def existe(self, titulo_libro: str) -> bool:
#     try:
#         GestionLibros.buscar_libro(titulo_libro)
#         return True
#     except ValueError:
#         return False

# def libro_prestado(self, titulo_libro: str) -> bool:
#     for prestamo in self.prestamos:
#         if prestamo.titulo_libro == titulo_libro:
#             return True
#     return False

# def caducado(self, hoy: date) -> bool:
#     return hoy > self.fecha_devolucion

