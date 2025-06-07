import os
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from vistas.registro import Ui_contenedorCentral  # Usa el nombre correcto según tu .ui
from modelos.ConexionMYSQL import conectar
import mysql.connector  # Necesario para capturar errores específicos
import hashlib
from PyQt5.QtWidgets import QDesktopWidget

class VentanaRegistro(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_contenedorCentral()
        self.ui.setupUi(self)
        
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
        # ✅ Estilo visual
        ruta_estilo = os.path.join("estilos", "estilo.qss")
        if os.path.exists(ruta_estilo):
            with open(ruta_estilo, "r") as f:
                self.setStyleSheet(f.read())

        # ✅ Configurar el logo
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

        if not nombre or not email or not contrasena or not confirmar:
            self.ui.lblError.setText("Todos los campos son obligatorios.")
            return

        if contrasena != confirmar:
            self.ui.lblError.setText("Las contraseñas no coinciden.")
            return

        # 🔐 ENCRIPTAR LA CONTRASEÑA:
        hash_contrasena = hashlib.sha256(contrasena.encode()).hexdigest()

        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Usuario (nombre, email, contraseña, rol)
                VALUES (%s, %s, %s, %s)
            """, (nombre, email, hash_contrasena, rol))
            conn.commit()
            self.ui.lblError.setText("Usuario registrado correctamente.")
            conn.close()
        except mysql.connector.IntegrityError:
            self.ui.lblError.setText("Ese email ya está registrado.")
        except Exception as e:
            self.ui.lblError.setText(f"⚠️ Error: {str(e)}")