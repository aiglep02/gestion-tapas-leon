import re
import hashlib
from modelos.dao.usuarioDAO import UsuarioDAO

class CrearUsuarioService:
    def __init__(self):
        self.usuario_dao = UsuarioDAO()  
        
    def crear_usuario(self, nombre, email, contrasena, rol):
        # Validaciones básicas
        if not nombre or not email or not contrasena or not rol:
            return "Todos los campos son obligatorios."

        if not re.fullmatch(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", email):
            return "Introduce un correo electrónico válido."

        if len(contrasena) < 8 or not re.search(r"[A-Za-z]", contrasena) or not re.search(r"[0-9]", contrasena):
            return "La contraseña debe tener al menos 8 caracteres, incluyendo letras y números."

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
