from modelos.dao.usuarioDAO import UsuarioDAO
from modelos.ConexionMYSQL import conectar

class UsuarioService:
    def __init__(self):
        self.conexion = conectar()
        self.usuario_dao = UsuarioDAO(self.conexion)

    def verificar_credenciales(self, email, contrasena, rol_ingresado):
        """
        Verifica si las credenciales son válidas y el rol coincide.
        Devuelve una tupla: (UsuarioVO, None) si todo está bien,
                            (None, mensaje_de_error) si hay fallo.
        """
        usuario_vo = self.usuario_dao.verificar_credenciales(email, contrasena)

        if usuario_vo is None:
            return None, "Credenciales incorrectas."

        rol_real = usuario_vo.rol.lower().strip()
        rol_ingresado = rol_ingresado.lower().strip()

        if rol_real != rol_ingresado:
            return None, f"El usuario no es {rol_ingresado}."

        return usuario_vo, None
