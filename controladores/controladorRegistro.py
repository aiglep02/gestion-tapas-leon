from modelos.logica.UsuarioService import UsuarioService

class ControladorRegistro:
    def __init__(self,conexion):
        self.usuario_service = UsuarioService(conexion)

    def registrar_usuario(self, nombre, email, contrasena, confirmar):
        """
        Intenta registrar un nuevo usuario.

        Parámetros:
        - nombre: str - Nombre del usuario
        - email: str - Correo electrónico
        - contrasena: str - Contraseña
        - confirmar: str - Confirmación de contraseña

        Retorna:
        - None si el registro fue exitoso.
        - str con mensaje de error si falló.
        """
        return self.usuario_service.registrar_usuario(nombre, email, contrasena, confirmar)
