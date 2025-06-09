from modelos.logica.UsuarioService import UsuarioService

class ControladorRegistro:
    def __init__(self):
        self.usuario_service = UsuarioService()

    def registrar_usuario(self, nombre, email, contrasena, confirmar):
        """
        Devuelve None si el registro fue exitoso.
        Devuelve un mensaje de error si algo falla.
        """
        return self.usuario_service.registrar_usuario(nombre, email, contrasena, confirmar)
