import sys
import os
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from vistas.login import Ui_Dialog  # Asegúrate de que login.ui fue convertido a login.py
from interfaces.VentanaAdminUsuarios import VentanaAdminUsuarios

class VentanaLogin(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # ✅ Cargar estilo desde QSS
        ruta_estilo = os.path.join("estilos", "estilo.qss")
        if os.path.exists(ruta_estilo):
            with open(ruta_estilo, "r") as f:
                self.setStyleSheet(f.read())
        else:
            print(f"[WARNING] No se encontró el archivo de estilo: {ruta_estilo}")

        # 🖼️ Configuración del logo (centrado, no achatado)
        logo = self.ui.logo
        logo.setAlignment(Qt.AlignCenter)
        logo.setScaledContents(False)

        ruta_logo = os.path.join("interfaces", "logoGestionTapas.jpg")
        if os.path.exists(ruta_logo):
            pixmap = QPixmap(ruta_logo)
            pixmap = pixmap.scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo.setPixmap(pixmap)
        else:
            print(f"[ERROR] No se encontró el logo en: {ruta_logo}")

        # Ajustes de tamaño de la ventana
        self.setFixedSize(500, 600)

        # Conectar botones
        self.ui.btnLogin.clicked.connect(self.iniciar_sesion)
        self.ui.botonRegistro.clicked.connect(self.registrarse)
        self.ui.botonAnonimo.clicked.connect(self.entrar_anonimo)

    def iniciar_sesion(self):
        usuario = self.ui.lineEdit.text()
        contrasena = self.ui.lineEdit_2.text()

        if usuario == "admin" and contrasena == "1234":
            self.ui.labelError.setText("Inicio correcto.")
            self.close()

            self.ventana_admin = VentanaAdminUsuarios()
            self.ventana_admin.show()
        else:
            self.ui.labelError.setText("Usuario o contraseña incorrectos.")

    def registrarse(self):
        from controladores.controladorRegistro import VentanaRegistro
        registro = VentanaRegistro()
        registro.exec_()

    def entrar_anonimo(self):
        self.ui.labelError.setText("Entraste como invitado.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaLogin()
    ventana.show()
    sys.exit(app.exec_())
