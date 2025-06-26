import re
from modelos.logica.UsuarioService import UsuarioService

class ControladorRegistro:
    def __init__(self):
        self.usuario_service = UsuarioService() 

    def registrar_usuario(self, nombre, email, contrasena, confirmar):
        """
        Intenta registrar un nuevo usuario con validaciones básicas.

        Retorna:
        - None si el registro fue exitoso.
        - str con mensaje de error si falló.
        """

        # 🔍 Validaciones de formato → deben estar en el controlador
        if not nombre or not email or not contrasena or not confirmar:
            return "Todos los campos son obligatorios."

        if contrasena != confirmar:
            return "Las contraseñas no coinciden."

        if not re.fullmatch(r"[a-zA-Z0-9_.+-]+@gmail\.com", email):
            return "Introduce un correo electrónico válido."

        if len(contrasena) < 8 or not re.search(r"[A-Za-z]", contrasena) or not re.search(r"[0-9]", contrasena):
            return "La contraseña debe tener al menos 8 caracteres, incluyendo letras y números."

        # ✅ Una vez validado, se llama al Service
        return self.usuario_service.registrar_usuario(nombre, email, contrasena)
