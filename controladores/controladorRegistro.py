import os
import re
import hashlib
import mysql.connector
import smtplib
import random
from email.message import EmailMessage
from PyQt5.QtWidgets import QDialog, QDesktopWidget, QInputDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from vistas.registro import Ui_contenedorCentral
from modelos.ConexionMYSQL import conectar
from modelos.dao.usuarioDAO import UsuarioDAO


class VentanaRegistro(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_contenedorCentral()
        self.ui.setupUi(self)

        # ✅ Centrar ventana
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        # ✅ Aplicar estilo
        ruta_estilo = os.path.join("estilos", "estilo.qss")
        if os.path.exists(ruta_estilo):
            with open(ruta_estilo, "r") as f:
                self.setStyleSheet(f.read())

        # ✅ Configurar logo
        logo = self.ui.logo
        logo.setAlignment(Qt.AlignCenter)
        logo.setScaledContents(False)

        ruta_logo = os.path.join("interfaces", "logoGestionTapas.jpg")
        if os.path.exists(ruta_logo):
            pixmap = QPixmap(ruta_logo)
            pixmap = pixmap.scaled(250, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo.setPixmap(pixmap)

        # ✅ Forzar el ComboBox a "cliente" y desactivarlo
        if hasattr(self.ui, "comboRol"):
            self.ui.comboRol.clear()
            self.ui.comboRol.addItem("cliente")
            self.ui.comboRol.setEnabled(False)

        # ✅ Conectar botón de registro
        self.ui.btnRegistrarse.clicked.connect(self.registrar_usuario)

    def registrar_usuario(self):
        nombre = self.ui.txtNombre.text()
        email = self.ui.txtEmail.text()
        contrasena = self.ui.txtContrasena.text()
        confirmar = self.ui.txtContrasena2.text()
        rol = "cliente"  # ⬅️ FORZAMOS el rol a "cliente" siempre

        # ✅ Validaciones básicas
        if not nombre or not email or not contrasena or not confirmar:
            self.ui.lblError.setText("Todos los campos son obligatorios.")
            return

        if contrasena != confirmar:
            self.ui.lblError.setText("Las contraseñas no coinciden.")
            return

        if not re.fullmatch(r"[a-zA-Z0-9_.+-]+@gmail\.com", email):
            self.ui.lblError.setText("Introduce un correo electrónico válido.")
            return

        if len(contrasena) < 8 or not re.search(r"[A-Za-z]", contrasena) or not re.search(r"[0-9]", contrasena):
            self.ui.lblError.setText("La contraseña debe tener al menos 8 caracteres, incluyendo letras y números.")
            return

        hash_contrasena = hashlib.sha256(contrasena.encode()).hexdigest()

        try:
            conn = conectar()
            usuario_dao = UsuarioDAO(conn)

            if usuario_dao.email_existente(email):
                self.ui.lblError.setText("Ese email ya está registrado.")
                conn.close()
                return
            if usuario_dao.nombre_existente(nombre):
                self.ui.lblError.setText("Ese nombre de usuario ya está en uso.")
                conn.close()
                return

            # ✅ Generar y enviar código de verificación
            codigo = str(random.randint(100000, 999999))
            enviar_codigo_verificacion(email, nombre, codigo)

            # ✅ Mostrar cuadro de entrada para el código
            introducido, ok = QInputDialog.getText(self, "Verificación de Email",
                f"Hemos enviado un código a {email}. Introduce el código:")

            if not ok or introducido != codigo:
                self.ui.lblError.setText("⚠️ Código incorrecto. Registro cancelado.")
                conn.close()
                return

            # ✅ Insertar usuario solo si el código es correcto
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO usuario (nombre, email, contraseña, rol)
                VALUES (%s, %s, %s, %s)
            """, (nombre, email, hash_contrasena, rol))
            conn.commit()
            self.ui.lblError.setText("✅ Usuario registrado correctamente.")
            conn.close()

        except mysql.connector.IntegrityError:
            self.ui.lblError.setText("Ese email ya está registrado.")
        except Exception as e:
            self.ui.lblError.setText(f"⚠️ Error: {str(e)}")


# ✅ Función para enviar código de verificación
def enviar_codigo_verificacion(destinatario, nombre_usuario, codigo):
    remitente = "trinialbaiglesias@gmail.com"
    contraseña_app = "xzol rnji nwdh yxbq"

    msg = EmailMessage()
    msg["Subject"] = "Código de verificación - Gestión de Tapas"
    msg["From"] = remitente
    msg["To"] = destinatario
    msg.set_content(f"Hola {nombre_usuario},\n\nTu código de verificación es: {codigo}\n\nIntroduce este código para confirmar tu registro.")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(remitente, contraseña_app)
            smtp.send_message(msg)
        print("✅ Código enviado correctamente")
    except Exception as e:
        print(f"⚠️ Error al enviar código: {str(e)}")
