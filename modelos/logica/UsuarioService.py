import re
import hashlib
import random
import smtplib
from email.message import EmailMessage
from PyQt5.QtWidgets import QInputDialog

from modelos.ConexionMYSQL import conectar
from modelos.dao.usuarioDAO import UsuarioDAO
from modelos.vo.usuarioVO import UsuarioVO

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

    def registrar_usuario(self, nombre, email, contrasena, confirmar):
        """
        Registra un nuevo usuario tras validaciones y verificación por correo.
        Devuelve None si fue exitoso, o un mensaje de error si algo falla.
        """
        if not nombre or not email or not contrasena or not confirmar:
            return "Todos los campos son obligatorios."

        if contrasena != confirmar:
            return "Las contraseñas no coinciden."

        if not re.fullmatch(r"[a-zA-Z0-9_.+-]+@gmail\.com", email):
            return "Introduce un correo electrónico válido."

        if len(contrasena) < 8 or not re.search(r"[A-Za-z]", contrasena) or not re.search(r"[0-9]", contrasena):
            return "La contraseña debe tener al menos 8 caracteres, incluyendo letras y números."

        if self.usuario_dao.email_existente(email):
            return "Ese email ya está registrado."

        if self.usuario_dao.nombre_existente(nombre):
            return "Ese nombre de usuario ya está en uso."

        # Envío de código de verificación
        codigo = str(random.randint(100000, 999999))
        if not self.enviar_codigo_verificacion(email, nombre, codigo):
            return "No se pudo enviar el código de verificación."

        introducido, ok = QInputDialog.getText(None, "Verificación de Email",
            f"Hemos enviado un código a {email}. Introduce el código:")

        if not ok or introducido != codigo:
            return "⚠️ Código incorrecto. Registro cancelado."

        hash_contrasena = hashlib.sha256(contrasena.encode()).hexdigest()

        usuario_vo = UsuarioVO(
            id_usuario=None,
            nombre=nombre,
            email=email,
            rol="cliente"
        )

        try:
            self.usuario_dao.insertar_usuario(usuario_vo, hash_contrasena)
            return None  # Éxito
        except Exception as e:
            return f"⚠️ Error: {str(e)}"

    def enviar_codigo_verificacion(self, destinatario, nombre_usuario, codigo):
        remitente = "gestion.tapas.leon@gmail.com"
        contraseña_app = "nclp rqwb fyvd flxn"

        msg = EmailMessage()
        msg["Subject"] = "Código de verificación - Gestión de Tapas"
        msg["From"] = remitente
        msg["To"] = destinatario

        msg.set_content(f"""Estimado/a {nombre_usuario},

¡Gracias por registrarte en "Gestión de Tapas León"! 🍻
Tu código de verificación es: 👉 {codigo} 👈

Si no has solicitado este registro, puedes ignorar este mensaje.

El equipo de Gestión de Tapas León 🦁
""")

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(remitente, contraseña_app)
                smtp.send_message(msg)
            return True
        except Exception as e:
            print(f"[ERROR] al enviar email: {e}")
            return False
