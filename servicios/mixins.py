import json, csv
from pathlib import Path
from typing import Iterable

class ExportarMixin:
    def exportar_json(self, ruta: Path) -> None:
        with open(ruta, 'w', encoding='utf-8') as f:
            json.dump(self.__dict__, f, ensure_ascii=False, indent=4)

    def exportar_csv(self, ruta: Path) -> None:
        with open(ruta, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(self.__dict__.keys())
            writer.writerow(self.__dict__.values())