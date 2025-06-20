from modelos.logica.CrearUsuarioService import CrearUsuarioService

class ControladorCrearUsuario:
    def __init__(self, conexion):
        self.service = CrearUsuarioService(conexion)

    def crear_usuario(self, nombre, email, contrasena, rol):
        return self.service.crear_usuario(nombre, email, contrasena, rol)
