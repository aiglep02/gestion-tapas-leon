import hashlib
from modelos.dao.usuarioDAO import UsuarioDAO

class CrearUsuarioService:
    def __init__(self):
        self.usuario_dao = UsuarioDAO()

    def crear_usuario(self, nombre, email, contrasena, rol):
        if self.usuario_dao.email_existente(email):
            return "Ese email ya está registrado."

        if self.usuario_dao.nombre_existente(nombre):
            return "Ese nombre de usuario ya está en uso."

        contrasena_hash = hashlib.sha256(contrasena.encode()).hexdigest()

        try:
            self.usuario_dao.insertar_usuario_manual(nombre, email, contrasena_hash, rol)
            return None  # Éxito
        except Exception as e:
            return f"Error al crear usuario: {str(e)}"
