from modelos.ConexionMYSQL import conectar
from modelos.dao.usuarioDAO import UsuarioDAO
from modelos.vo.usuarioVO import UsuarioVO

class AdminUsuarioService:
    def __init__(self):
        self.conexion = conectar()
        self.usuario_dao = UsuarioDAO(self.conexion)

    def obtener_todos_los_usuarios(self):
        """
        Devuelve una lista de UsuarioVO con todos los usuarios del sistema.
        """
        return self.usuario_dao.obtener_todos()

    def eliminar_usuario_por_id(self, id_usuario):
        """
        Elimina un usuario por su ID.
        """
        self.usuario_dao.eliminar_por_id(id_usuario)

    def actualizar_rol_usuario(self, id_usuario, nuevo_rol):
        """
        Cambia el rol de un usuario dado su ID.
        """
        self.usuario_dao.actualizar_rol(id_usuario, nuevo_rol)
