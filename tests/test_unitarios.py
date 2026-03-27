import unittest
from datetime import date, timedelta
from modelos.libro import Libro
from modelos.usuario import Usuario
from modelos.prestamo import Prestamo
from servicios.gestion_libros import GestionLibros
from servicios.gestion_usuarios import GestionUsuarios
from servicios.gestion_prestamos import GestionPrestamos
from servicios.multas import MultaService


class TestLibro(unittest.TestCase):
    def test_crear_libro(self):
        libro = Libro(titulo="El Quijote", autor="Cervantes", isbn="12345")
        self.assertEqual(libro.titulo, "El Quijote")
        self.assertEqual(libro.autor, "Cervantes")
        self.assertEqual(libro.isbn, "12345")

    def test_str_libro(self):
        libro = Libro(titulo="1984", autor="Orwell", isbn="67890")
        expected = "1984 - Orwell (ISBN: 67890)"
        self.assertEqual(str(libro), expected)


class TestUsuario(unittest.TestCase):
    def test_crear_usuario(self):
        usuario = Usuario(nombre="Jordi", id_usuario=1)
        self.assertEqual(usuario.nombre, "Jordi")
        self.assertEqual(usuario.id_usuario, 1)

    def test_str_usuario(self):
        usuario = Usuario(nombre="María", id_usuario=2)
        expected = "María (ID: 2)"
        self.assertEqual(str(usuario), expected)

    def test_registrar_evento(self):
        usuario = Usuario(nombre="Pedro", id_usuario=3)
        usuario.registrar_evento("Préstamo realizado")
        self.assertIn("Préstamo realizado", usuario.historial())

    def test_historial_usuario(self):
        usuario = Usuario(nombre="Ana", id_usuario=4)
        usuario.registrar_evento("Evento 1")
        usuario.registrar_evento("Evento 2")
        self.assertEqual(len(usuario.historial()), 2)


class TestPrestamo(unittest.TestCase):
    def test_crear_prestamo(self):
        hoy = date.today()
        prestamo = Prestamo(id_usuario=1, isbn="12345", fecha_prestamo=hoy)
        self.assertEqual(prestamo.id_usuario, 1)
        self.assertEqual(prestamo.isbn, "12345")
        self.assertEqual(prestamo.fecha_prestamo, hoy)
        self.assertIsNone(prestamo.fecha_devolucion)

    def test_prestamo_no_caducado(self):
        hoy = date.today()
        prestamo = Prestamo(id_usuario=1, isbn="12345", fecha_prestamo=hoy, dias_plazo=14)
        self.assertFalse(prestamo.caducado(hoy + timedelta(days=5)))

    def test_prestamo_caducado(self):
        hoy = date.today()
        hace_20_dias = hoy - timedelta(days=20)
        prestamo = Prestamo(id_usuario=1, isbn="12345", fecha_prestamo=hace_20_dias, dias_plazo=14)
        self.assertTrue(prestamo.caducado(hoy))

    def test_prestamo_devuelto_no_caducado(self):
        hoy = date.today()
        prestamo = Prestamo(
            id_usuario=1,
            isbn="12345",
            fecha_prestamo=hoy - timedelta(days=20),
            dias_plazo=14,
            fecha_devolucion=hoy
        )
        self.assertFalse(prestamo.caducado(hoy))


class TestGestionLibros(unittest.TestCase):
    def setUp(self):
        self.gestion = GestionLibros()

    def test_agregar_libro(self):
        libro = self.gestion.agregar_libro("El Quijote", "Cervantes", "12345")
        self.assertEqual(libro.titulo, "El Quijote")
        self.assertIn("12345", self.gestion.libros)

    def test_agregar_libro_duplicado(self):
        self.gestion.agregar_libro("El Quijote", "Cervantes", "12345")
        with self.assertRaises(ValueError):
            self.gestion.agregar_libro("Otra novela", "Otro autor", "12345")

    def test_buscar_libro(self):
        self.gestion.agregar_libro("1984", "Orwell", "67890")
        libro = self.gestion.buscar_libro("67890")
        self.assertEqual(libro.titulo, "1984")

    def test_buscar_libro_no_existe(self):
        with self.assertRaises(ValueError):
            self.gestion.buscar_libro("99999")

    def test_listar_libros(self):
        self.gestion.agregar_libro("El Quijote", "Cervantes", "12345")
        self.gestion.agregar_libro("1984", "Orwell", "67890")
        libros = list(self.gestion.listar_libros())
        self.assertEqual(len(libros), 2)

    def test_baja_libro(self):
        self.gestion.agregar_libro("El Quijote", "Cervantes", "12345")
        self.gestion.baja_libro("12345")
        with self.assertRaises(ValueError):
            self.gestion.buscar_libro("12345")


class TestGestionUsuarios(unittest.TestCase):
    def setUp(self):
        self.gestion = GestionUsuarios()

    def test_agregar_usuario(self):
        usuario = self.gestion.agregar_usuario("Jordi", 1)
        self.assertEqual(usuario.nombre, "Jordi")
        self.assertIn(1, self.gestion.usuarios)

    def test_agregar_usuario_duplicado(self):
        self.gestion.agregar_usuario("Jordi", 1)
        with self.assertRaises(ValueError):
            self.gestion.agregar_usuario("María", 1)

    def test_obtener_usuario(self):
        self.gestion.agregar_usuario("María", 2)
        usuario = self.gestion.obtener_usuario(2)
        self.assertEqual(usuario.nombre, "María")

    def test_obtener_usuario_no_existe(self):
        with self.assertRaises(ValueError):
            self.gestion.obtener_usuario(999)

    def test_listar_usuarios(self):
        self.gestion.agregar_usuario("Jordi", 1)
        self.gestion.agregar_usuario("María", 2)
        usuarios = self.gestion.listar_usuarios()
        self.assertEqual(len(usuarios), 2)

    def test_eliminar_usuario(self):
        self.gestion.agregar_usuario("Jordi", 1)
        self.gestion.eliminar_usuario(1)
        with self.assertRaises(ValueError):
            self.gestion.obtener_usuario(1)


class TestGestionPrestamos(unittest.TestCase):
    def setUp(self):
        self.gestion = GestionPrestamos()
        self.gestion_libros = GestionLibros()
        self.gestion_libros.agregar_libro("El Quijote", "Cervantes", "12345")

    def test_realizar_prestamo(self):
        prestamo = self.gestion.realizar_prestamo(self.gestion_libros, 1, "12345")
        self.assertEqual(prestamo.id_usuario, 1)
        self.assertEqual(prestamo.isbn, "12345")
        self.assertIn(prestamo, self.gestion.prestamos)

    def test_realizar_prestamo_libro_no_existe(self):
        with self.assertRaises(ValueError):
            self.gestion.realizar_prestamo(self.gestion_libros, 1, "99999")

    def test_realizar_prestamo_libro_ya_prestado(self):
        self.gestion.realizar_prestamo(self.gestion_libros, 1, "12345")
        with self.assertRaises(ValueError):
            self.gestion.realizar_prestamo(self.gestion_libros, 2, "12345")

    def test_listar_prestamos(self):
        self.gestion.realizar_prestamo(self.gestion_libros, 1, "12345")
        prestamos = self.gestion.listar_prestamos()
        self.assertEqual(len(prestamos), 1)

    def test_devolver_libro_a_tiempo(self):
        self.gestion.realizar_prestamo(self.gestion_libros, 1, "12345")
        multa = self.gestion.devolver_libro(1, "12345")
        self.assertIsNone(multa)
        self.assertEqual(len(self.gestion.prestamos), 0)
        self.assertEqual(len(self.gestion.historico), 1)

    def test_devolver_libro_con_retraso(self):
        hoy = date.today()
        prestamo = Prestamo(id_usuario=1, isbn="12345", fecha_prestamo=hoy - timedelta(days=20), dias_plazo=14)
        self.gestion.prestamos.append(prestamo)
        
        multa = self.gestion.devolver_libro(1, "12345")
        self.assertIsNotNone(multa)
        self.assertGreater(multa, 0)

    def test_devolver_libro_no_existe(self):
        with self.assertRaises(ValueError):
            self.gestion.devolver_libro(999, "12345")

    def test_prestamos_caducados_no_devueltos(self):
        hoy = date.today()
        hace_20_dias = hoy - timedelta(days=20)
        prestamo = Prestamo(id_usuario=1, isbn="12345", fecha_prestamo=hace_20_dias, dias_plazo=14)
        self.gestion.prestamos.append(prestamo)
        
        caducados = self.gestion.prestamos_caducados_no_devueltos(hoy)
        self.assertEqual(len(caducados), 1)


class TestMultaService(unittest.TestCase):
    def test_singleton_instance(self):
        multa1 = MultaService()
        multa2 = MultaService()
        self.assertIs(multa1, multa2)

    def test_asignar_multa(self):
        multa_service = MultaService()
        multa_service.multas = {}
        monto = multa_service.asignar_multa(1, "12345", 5, tasa=1.5)
        self.assertEqual(monto, 7.5)
        self.assertIn(1, multa_service.multas)

    def test_obtener_multas_usuario(self):
        multa_service = MultaService()
        multa_service.multas = {}
        multa_service.asignar_multa(1, "12345", 5, tasa=1.5)
        multa_service.asignar_multa(1, "67890", 3, tasa=1.5)
        
        multas = multa_service.obtener_multas(1)
        self.assertEqual(len(multas), 2)

    def test_obtener_todas_multas(self):
        multa_service = MultaService()
        multa_service.multas = {}
        multa_service.asignar_multa(1, "12345", 5, tasa=1.5)
        multa_service.asignar_multa(2, "67890", 3, tasa=1.5)
        
        todas = multa_service.obtener_multas()
        self.assertEqual(len(todas), 2)


if __name__ == '__main__':
    unittest.main()
