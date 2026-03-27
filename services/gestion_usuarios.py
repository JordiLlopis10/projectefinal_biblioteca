from modelos.usuario import Usuario
from servicios.decoradores import loggear_accion, requiere_campos
from servicios.mixins import ExportarMixin, ImportarMixins

class GestionUsuarios(ExportarMixin, ImportarMixins):
    def __init__(self):
        self.usuarios = {}

    @loggear_accion
    @requiere_campos('nombre', 'id_usuario')
    def agregar_usuario(self, nombre: str, id_usuario: int) -> Usuario:
        if id_usuario in self.usuarios:
            raise ValueError(f"El ID de usuario {id_usuario} ya existe.")
        nuevo_usuario = Usuario(nombre=nombre, id_usuario=id_usuario)
        self.usuarios[id_usuario] = nuevo_usuario
        return nuevo_usuario

    @loggear_accion
    def obtener_usuario(self, id_usuario: int) -> Usuario:
        if id_usuario not in self.usuarios:
            raise ValueError(f"No se encontró el usuario con ID {id_usuario}.")
        return self.usuarios[id_usuario]

    @loggear_accion
    def eliminar_usuario(self, id_usuario: int) -> None:
        if id_usuario not in self.usuarios:
            raise ValueError(f"No se encontró el usuario con ID {id_usuario}.")
        del self.usuarios[id_usuario]

    def listar_usuarios(self) -> list[Usuario]:
        return list(self.usuarios.values())

    def exportar_usuarios(self, ruta):
        return super().exportar_usuarios(ruta)

    def importar_usuarios(self, ruta):
        return super().importar_usuarios(ruta)