from modelos.logica.CrearUsuarioService import CrearUsuarioService

class ControladorCrearUsuario:
    def __init__(self):
        self.service = CrearUsuarioService()  

    def crear_usuario(self, nombre, email, contrasena, rol):
        return self.service.crear_usuario(nombre, email, contrasena, rol)
