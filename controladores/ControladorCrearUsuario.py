from modelos.logica.CrearUsuarioService import CrearUsuarioService

class ControladorCrearUsuario:
    def __init__(self):
        self.service = CrearUsuarioService()

    def crear_usuario(self, nombre, email, contrasena, rol):
        """
        Llama al servicio para crear usuario.
        Devuelve None si éxito, o mensaje de error.
        """
        return self.service.crear_usuario(nombre, email, contrasena, rol)
