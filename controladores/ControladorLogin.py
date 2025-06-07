from modelos.dao.usuarioDAO import UsuarioDAO

class ControladorLogin:
    def __init__(self, conexion):
        self.usuario_dao = UsuarioDAO(conexion)

    def verificar_credenciales(self, email, contrasena):
        return self.usuario_dao.verificar_credenciales(email, contrasena)