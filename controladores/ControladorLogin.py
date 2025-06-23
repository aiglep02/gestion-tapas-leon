from modelos.logica.UsuarioService import UsuarioService

class ControladorLogin:
    def __init__(self, conexion):
        self.usuario_service = UsuarioService(conexion)

    def verificar_credenciales(self, email, contrasena, rol_ingresado):
        """
        Devuelve (UsuarioVO, None) si todo es correcto,
        o (None, mensaje de error) si falla algo.
        """
        return self.usuario_service.verificar_credenciales(email, contrasena, rol_ingresado)
