import hashlib
import random
import smtplib
from email.message import EmailMessage
from PyQt5.QtWidgets import QInputDialog

from modelos.dao.usuarioDAO import UsuarioDAO
from modelos.vo.usuarioVO import UsuarioVO

class UsuarioService:
    def __init__(self):
        self.usuario_dao = UsuarioDAO()

    def verificar_credenciales(self, email, contrasena, rol_ingresado):
        usuario_vo = self.usuario_dao.verificar_credenciales(email, contrasena)

        if usuario_vo is None:
            return None, "Credenciales incorrectas."

        rol_real = usuario_vo.rol.lower().strip()
        rol_ingresado = rol_ingresado.lower().strip()

        if rol_real != rol_ingresado:
            return None, f"El usuario no es {rol_ingresado}."

        return usuario_vo, None

    def registrar_usuario(self, nombre, email, contrasena):
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
