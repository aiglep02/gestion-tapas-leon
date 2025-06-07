import os
import re
import hashlib
import mysql.connector
from PyQt5.QtWidgets import QDialog, QDesktopWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from vistas.registro import Ui_contenedorCentral
from modelos.ConexionMYSQL import conectar
from modelos.dao.usuarioDAO import UsuarioDAO  # ⬅️ ¡Nuevo import!

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

        # ✅ Conectar botón de registro
        self.ui.btnRegistrarse.clicked.connect(self.registrar_usuario)

    def registrar_usuario(self):
        nombre = self.ui.txtNombre.text()
        email = self.ui.txtEmail.text()
        contrasena = self.ui.txtContrasena.text()
        confirmar = self.ui.txtContrasena2.text()
        rol = self.ui.comboRol.currentText()

        # ✅ Validaciones básicas
        if not nombre or not email or not contrasena or not confirmar:
            self.ui.lblError.setText("Todos los campos son obligatorios.")
            return

        if contrasena != confirmar:
            self.ui.lblError.setText("Las contraseñas no coinciden.")
            return

        # ✅ Validación de correo
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            self.ui.lblError.setText("Introduce un correo electrónico válido.")
            return

        # ✅ Validación de contraseña fuerte
        if len(contrasena) < 8 or not re.search(r"[A-Za-z]", contrasena) or not re.search(r"[0-9]", contrasena):
            self.ui.lblError.setText("La contraseña debe tener al menos 8 caracteres, incluyendo letras y números.")
            return

        # 🔐 Encriptar la contraseña
        hash_contrasena = hashlib.sha256(contrasena.encode()).hexdigest()

        try:
            conn = conectar()
            usuario_dao = UsuarioDAO(conn)  # ⬅️ Usamos DAO en lugar de SQL directo

            # ✅ Verificar si el email ya está registrado
            if usuario_dao.email_existente(email):
                self.ui.lblError.setText("Ese email ya está registrado.")
                conn.close()
                return

            # ✅ Insertar nuevo usuario
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO usuario (nombre, email, contraseña, rol)
                VALUES (%s, %s, %s, %s)
            """, (nombre, email, hash_contrasena, rol))
            conn.commit()
            self.ui.lblError.setText("Usuario registrado correctamente.")
            conn.close()

        except mysql.connector.IntegrityError:
            self.ui.lblError.setText("Ese email ya está registrado.")
        except Exception as e:
            self.ui.lblError.setText(f"⚠️ Error: {str(e)}")
