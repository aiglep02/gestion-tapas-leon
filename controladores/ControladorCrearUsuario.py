import re
from modelos.logica.CrearUsuarioService import CrearUsuarioService

class ControladorCrearUsuario:
    def __init__(self):
        self.service = CrearUsuarioService()

    def crear_usuario(self, nombre, email, contrasena, rol):
        # 🔍 Validaciones que pertenecen al controlador
        if not nombre or not email or not contrasena or not rol:
            return "Todos los campos son obligatorios."

        if not re.fullmatch(r"[a-zA-Z0-9_.+-]+@gmail\.com", email):
            return "Introduce un correo electrónico válido."

        if len(contrasena) < 8 or not re.search(r"[A-Za-z]", contrasena) or not re.search(r"[0-9]", contrasena):
            return "La contraseña debe tener al menos 8 caracteres, incluyendo letras y números."

        return self.service.crear_usuario(nombre, email, contrasena, rol)
