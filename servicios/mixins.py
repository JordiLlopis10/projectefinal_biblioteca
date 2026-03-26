import json, csv
from pathlib import Path
from dataclasses import asdict
class ExportarMixin:

    def exportar_json(self, ruta: Path) -> None:
        if hasattr(self, "libros"):
            data = [asdict(libro) for libro in self.libros.values()]
        else:
            data = self.__dict__

        with open(ruta, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def exportar_csv(self, ruta: Path) -> None:
        with open(ruta, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if hasattr(self, "libros") and self.libros:
                # Escribir encabezados
                writer.writerow(['titulo', 'autor', 'isbn'])
                # Escribir cada libro como fila
                for libro in self.libros.values():
                    writer.writerow([libro.titulo, libro.autor, libro.isbn])
            else:
                # Fallback para otros objetos
                writer.writerow(self.__dict__.keys())
                writer.writerow(self.__dict__.values())


class ImportarMixins:

    def importar_json(self, ruta: Path) -> None:
        from modelos.libro import Libro
        
        with open(ruta, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            if isinstance(data, list):
                for item in data:
                    libro = Libro(**item)
                    if hasattr(self, 'libros'):
                        self.libros[libro.isbn] = libro
            elif isinstance(data, dict):
                for key, item in data.items():
                    libro = Libro(**item)
                    if hasattr(self, 'libros'):
                        self.libros[libro.isbn] = libro



    def importar_csv(self, ruta: Path) -> None:
        from modelos.libro import Libro
        
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