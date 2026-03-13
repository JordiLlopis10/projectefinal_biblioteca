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
            writer.writerow(self.__dict__.keys())
            writer.writerow(self.__dict__.values())