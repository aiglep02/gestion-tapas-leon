from modelos.logica.AdminUsuarioService import AdminUsuarioService

class ControladorAdminUsuarios:
    def __init__(self, conexion):
        self.usuario_service = AdminUsuarioService(conexion)

    def listar_usuarios(self):
        return self.usuario_service.obtener_todos_los_usuarios()

    def eliminar_usuario(self, id_usuario):
        self.usuario_service.eliminar_usuario_por_id(id_usuario)

    def cambiar_rol(self, id_usuario, nuevo_rol):
        self.usuario_service.actualizar_rol_usuario(id_usuario, nuevo_rol)
