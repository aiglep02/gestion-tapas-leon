import sys
import os
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from vistas.login import Ui_Dialog  # generado desde login.ui

class VentanaLogin(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # 🪟 Ajuste de ventana general
        self.setFixedSize(500, 600)  # Espacio más vertical para dejar sitio al logo

        # 🖼️ Configuración del logo
        logo = self.ui.logo
        logo.setAlignment(Qt.AlignCenter)
        logo.setScaledContents(False)  # Desactiva el estiramiento forzado

        ruta_logo = os.path.join("interfaces", "logoGestionTapas.jpg")
        if os.path.exists(ruta_logo):
            pixmap = QPixmap(ruta_logo)
            # Usamos un cuadrado visual para que no se deforme
            pixmap = pixmap.scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo.setPixmap(pixmap)
        else:
            print(f"[ERROR] No se encontró el logo en: {ruta_logo}")

        # 🔘 Botones funcionales
        self.ui.btnLogin.clicked.connect(self.iniciar_sesion)
        self.ui.botonRegistro.clicked.connect(self.registrarse)
        self.ui.botonAnonimo.clicked.connect(self.entrar_anonimo)

    def iniciar_sesion(self):
        usuario = self.ui.lineEdit.text()
        contrasena = self.ui.lineEdit_2.text()
        if usuario == "admin" and contrasena == "1234":
            self.ui.labelError.setText("Inicio correcto.")
        else:
            self.ui.labelError.setText("Usuario o contraseña incorrectos.")

    def registrarse(self):
        self.ui.labelError.setText("Función de registro no implementada.")

    def entrar_anonimo(self):
        self.ui.labelError.setText("Entraste como invitado.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaLogin()
    ventana.show()
    sys.exit(app.exec_())
