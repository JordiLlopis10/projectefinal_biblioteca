# Este módulo contiene mixins para exportar e importar datos en formatos JSON y CSV, facilitando la persistencia y recuperación de información en la aplicación.
import json, csv
from pathlib import Path
from dataclasses import asdict
from datetime import date

class ExportarMixin:
    """Mixin que proporciona funcionalidad de exportación en JSON y CSV."""

    def exportar_json(self, ruta: Path) -> None:
        """Exporta datos de libros, usuarios o histórico a archivo JSON."""
        if hasattr(self, "libros"):
            data = [asdict(libro) for libro in self.libros.values()]
        else:
            data = self.__dict__

        with open(ruta, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def exportar_csv(self, ruta: Path) -> None:
        """Exporta datos de libros a archivo CSV."""
        with open(ruta, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if hasattr(self, "libros") and self.libros:
                writer.writerow(['titulo', 'autor', 'isbn'])
                for libro in self.libros.values():
                    writer.writerow([libro.titulo, libro.autor, libro.isbn])
            else:
                writer.writerow(self.__dict__.keys())
                writer.writerow(self.__dict__.values())

    def exportar_usuarios(self, ruta: Path) -> None:
        """Exporta usuarios a archivo JSON."""
        if not hasattr(self, 'usuarios'):
            raise AttributeError('El objeto no tiene usuarios para exportar.')

        data = [asdict(usuario) for usuario in self.usuarios.values()]
        with open(ruta, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def exportar_historico(self, ruta: Path) -> None:
        """Exporta histórico de préstamos a archivo JSON con fechas serializadas."""
        if not hasattr(self, 'historico'):
            raise AttributeError('El objeto no tiene historico de prestamos para exportar.')

        def serializar_historico(prestamo):
            data = asdict(prestamo)
            data['fecha_prestamo'] = data['fecha_prestamo'].isoformat() if data['fecha_prestamo'] else None
            data['fecha_devolucion'] = data.get('fecha_devolucion').isoformat() if data.get('fecha_devolucion') else None
            return data

        data = [serializar_historico(prestamo) for prestamo in self.historico]
        with open(ruta, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def exportar_usuarios_csv(self, ruta: Path) -> None:
        if not hasattr(self, 'usuarios'):
            raise AttributeError('El objeto no tiene usuarios para exportar.')

        with open(ruta, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['nombre', 'id_usuario'])
            for usuario in self.usuarios.values():
                writer.writerow([usuario.nombre, usuario.id_usuario])

    def importar_usuarios_csv(self, ruta: Path) -> None:
        from models.usuario import Usuario

        if not hasattr(self, 'usuarios'):
            self.usuarios = {}

        with open(ruta, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                usuario = Usuario(nombre=row['nombre'].strip(), id_usuario=int(row['id_usuario'].strip()))
                self.usuarios[usuario.id_usuario] = usuario

    def exportar_historico_csv(self, ruta: Path) -> None:
        if not hasattr(self, 'historico'):
            raise AttributeError('El objeto no tiene historico de prestamos para exportar.')

        with open(ruta, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id_usuario', 'isbn', 'fecha_prestamo', 'fecha_devolucion', 'dias_plazo', 'multa'])
            for prestamo in self.historico:
                writer.writerow([
                    prestamo.id_usuario,
                    prestamo.isbn,
                    prestamo.fecha_prestamo.isoformat() if prestamo.fecha_prestamo else '',
                    prestamo.fecha_devolucion.isoformat() if prestamo.fecha_devolucion else '',
                    prestamo.dias_plazo,
                    prestamo.multa if prestamo.multa is not None else ''
                ])

    def importar_historico_csv(self, ruta: Path) -> None:
        from models.prestamo import Prestamo

        if not hasattr(self, 'historico'):
            self.historico = []

        with open(ruta, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                tp = date.fromisoformat(row['fecha_prestamo'])
                td = date.fromisoformat(row['fecha_devolucion']) if row.get('fecha_devolucion') else None
                dias_plazo = int(row['dias_plazo']) if row.get('dias_plazo') else 14
                multa = float(row['multa']) if row.get('multa') else None
                prestamo = Prestamo(
                    id_usuario=int(row['id_usuario']),
                    isbn=row['isbn'],
                    fecha_prestamo=tp,
                    dias_plazo=dias_plazo,
                    fecha_devolucion=td,
                    multa=multa
                )
                self.historico.append(prestamo)


class ImportarMixins:

    def importar_json(self, ruta: Path) -> None:
        from models.libro import Libro
        
        with open(ruta, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            if isinstance(data, list):
                for item in data:
                    if 'isbn' in item and hasattr(self, 'libros'):
                        libro = Libro(**item)
                        self.libros[libro.isbn] = libro
                    elif 'id_usuario' in item and hasattr(self, 'usuarios'):
                        from models.usuario import Usuario
                        usuario = Usuario(**item)
                        self.usuarios[usuario.id_usuario] = usuario
                    elif 'fecha_prestamo' in item and hasattr(self, 'historico'):
                        from models.prestamo import Prestamo
                        item_copy = item.copy()
                        item_copy['fecha_prestamo'] = date.fromisoformat(item_copy['fecha_prestamo'])
                        if item_copy.get('fecha_devolucion'):
                            item_copy['fecha_devolucion'] = date.fromisoformat(item_copy['fecha_devolucion'])
                        self.historico.append(Prestamo(**item_copy))
            elif isinstance(data, dict):
                for key, item in data.items():
                    if 'isbn' in item and hasattr(self, 'libros'):
                        libro = Libro(**item)
                        self.libros[libro.isbn] = libro
                    elif 'id_usuario' in item and hasattr(self, 'usuarios'):
                        from models.usuario import Usuario
                        usuario = Usuario(**item)
                        self.usuarios[usuario.id_usuario] = usuario
                    elif 'fecha_prestamo' in item and hasattr(self, 'historico'):
                        from models.prestamo import Prestamo
                        item_copy = item.copy()
                        item_copy['fecha_prestamo'] = date.fromisoformat(item_copy['fecha_prestamo'])
                        if item_copy.get('fecha_devolucion'):
                            item_copy['fecha_devolucion'] = date.fromisoformat(item_copy['fecha_devolucion'])
                        self.historico.append(Prestamo(**item_copy))


    def importar_csv(self, ruta: Path) -> None:
        from models.libro import Libro
        
        if not hasattr(self, 'libros'):
            self.libros = {}

        with open(ruta, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                if not all(key in row for key in ['titulo', 'autor', 'isbn']):
                    print(f"Fila incompleta ignorada: {row}")
                    continue
                
                try:
                    libro = Libro(
                        titulo=row['titulo'].strip(),
                        autor=row['autor'].strip(),
                        isbn=row['isbn'].strip()
                    )
                    
                    self.libros[libro.isbn] = libro
                
                except Exception as e:
                    print(f"Error procesando fila {row}: {e}")

    def importar_usuarios(self, ruta: Path) -> None:
        from models.usuario import Usuario

        if not hasattr(self, 'usuarios'):
            self.usuarios = {}

        with open(ruta, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for item in data:
                usuario = Usuario(**item)
                self.usuarios[usuario.id_usuario] = usuario

    def importar_historico(self, ruta: Path) -> None:
        from models.prestamo import Prestamo

        if not hasattr(self, 'historico'):
            self.historico = []

        with open(ruta, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for item in data:
                item_copy = item.copy()
                item_copy['fecha_prestamo'] = date.fromisoformat(item_copy['fecha_prestamo'])
                if item_copy.get('fecha_devolucion'):
                    item_copy['fecha_devolucion'] = date.fromisoformat(item_copy['fecha_devolucion'])
                self.historico.append(Prestamo(**item_copy))