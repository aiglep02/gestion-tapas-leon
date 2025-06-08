from PyQt5.QtWidgets import (
    QDialog, QDesktopWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QMessageBox, QInputDialog
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import os, re, hashlib, smtplib, random
from email.message import EmailMessage
import mysql.connector

from vistas.registro import Ui_contenedorCentral
from modelos.ConexionMYSQL import conectar
from modelos.dao.usuarioDAO import UsuarioDAO
from vistas.login_view import VentanaLogin


class VentanaRegistro(QDialog):
    def __init__(self, coordinador=None):
        super().__init__()
        self.ui = Ui_contenedorCentral()
        self.ui.setupUi(self)
        self.coordinador = coordinador

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

        # ✅ Añadir botón de ayuda
        ayuda_layout = QHBoxLayout()
        ayuda_layout.setAlignment(Qt.AlignRight)
        boton_ayuda = QPushButton("?")
        boton_ayuda.setFixedSize(30, 30)
        boton_ayuda.setToolTip("Ayuda sobre el registro")
        boton_ayuda.clicked.connect(self.mostrar_ayuda)
        ayuda_layout.addWidget(boton_ayuda)
        self.ui.verticalLayout_2.addLayout(ayuda_layout)

        # ✅ Forzar el ComboBox a cliente y desactivarlo
        if hasattr(self.ui, "comboRol"):
            self.ui.comboRol.clear()
            self.ui.comboRol.addItem("cliente")
            self.ui.comboRol.setEnabled(False)

        # ✅ Conectar botones
        self.ui.btnRegistrarse.clicked.connect(self.registrar_usuario)

        # ✅ Botón "Salir" → volver al login
        if hasattr(self.ui, "btnCancelar"):
            self.ui.btnCancelar.clicked.connect(self.volver_al_login)

    def volver_al_login(self):
        self.close()
        self.login = VentanaLogin(self.coordinador)
        self.login.show()

    def mostrar_ayuda(self):
        QMessageBox.information(
            self,
            "Ayuda - Registro",
            "Para registrarte necesitas rellenar todos los campos:\n"
            "- Nombre de usuario único\n"
            "- Correo electrónico de Gmail válido\n"
            "- Contraseña con mínimo 8 caracteres, con letras y números\n\n"
            "Se te enviará un código al correo y deberás introducirlo para completar el registro.\n"
            "Solo se permiten registros de clientes. Los empleados y administradores deben ser añadidos por el administrador."
        )

    def registrar_usuario(self):
        nombre = self.ui.txtNombre.text()
        email = self.ui.txtEmail.text()
        contrasena = self.ui.txtContrasena.text()
        confirmar = self.ui.txtContrasena2.text()
        rol = "cliente"

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

            codigo = str(random.randint(100000, 999999))
            enviar_codigo_verificacion(email, nombre, codigo)

            introducido, ok = QInputDialog.getText(self, "Verificación de Email",
                f"Hemos enviado un código a {email}. Introduce el código:")

            if not ok or introducido != codigo:
                self.ui.lblError.setText("⚠️ Código incorrecto. Registro cancelado.")
                conn.close()
                return

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


def enviar_codigo_verificacion(destinatario, nombre_usuario, codigo):
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
        print("✅ Código enviado correctamente")
    except Exception as e:
        print(f"⚠️ Error al enviar código: {str(e)}")
