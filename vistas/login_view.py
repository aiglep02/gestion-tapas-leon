# vistas/login_view.py

from PyQt5.QtWidgets import QDialog, QDesktopWidget, QWidget, QVBoxLayout, QPushButton, QMessageBox, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from vistas.login import Ui_Dialog
import os

class VentanaLogin(QDialog):
    def __init__(self, coordinador):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.coordinador = coordinador

        # ✅ Establecer tamaño fijo razonable
        self.setFixedSize(500, 600)

        # ✅ Centrar ventana en pantalla
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        # ✅ Cargar logo desde archivo y mostrarlo centrado
        ruta_logo = os.path.join("interfaces", "logoGestionTapas.jpg")
        if os.path.exists(ruta_logo):
            pixmap_original = QPixmap(ruta_logo)
            if not pixmap_original.isNull():
                pixmap_escalado = pixmap_original.scaled(
                    450, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
                self.ui.logo.setPixmap(pixmap_escalado)

                # ✅ Centrar logo
                logo_container = QWidget()
                logo_layout = QVBoxLayout(logo_container)
                logo_layout.setAlignment(Qt.AlignCenter)
                logo_layout.addWidget(self.ui.logo)
                self.ui.verticalLayout.insertWidget(0, logo_container)
            else:
                print("[ERROR] Imagen vacía.")
        else:
            print(f"[ERROR] Imagen no encontrada: {ruta_logo}")

        # ✅ Añadir botón de ayuda
        ayuda_layout = QHBoxLayout()
        ayuda_layout.setAlignment(Qt.AlignRight)
        boton_ayuda = QPushButton("?")
        boton_ayuda.setFixedSize(30, 30)
        boton_ayuda.setToolTip("Ayuda sobre esta pantalla")
        boton_ayuda.clicked.connect(self.mostrar_ayuda)
        ayuda_layout.addWidget(boton_ayuda)
        self.ui.verticalLayout.insertLayout(0, ayuda_layout)

        # ✅ Conectar botones
        self.ui.btnLogin.clicked.connect(self.login)
        self.ui.botonRegistro.clicked.connect(self.abrir_registro)
        self.ui.botonAnonimo.clicked.connect(self.entrar_como_invitado)

    def login(self):
        email = self.ui.lineEdit.text()
        contrasena = self.ui.lineEdit_2.text()
        index = self.ui.comboRol.currentIndex()
        roles_internos = ["cliente", "empleado", "admin"]
        rol_seleccionado = roles_internos[index]
        self.coordinador.login(email, contrasena, rol_seleccionado, self)

    def mostrar_error(self, mensaje):
        self.ui.labelError.setText(mensaje)

    def abrir_registro(self):
        self.coordinador.mostrar_registro()

    def entrar_como_invitado(self):
        self.coordinador.mostrar_vista_invitado()

    def mostrar_ayuda(self):
        QMessageBox.information(
            self,
            "Ayuda - Inicio de Sesión",
            "Desde esta pantalla puedes:\n"
            "- Iniciar sesión con tu email, contraseña y rol correspondiente.\n"
            "- Registrarte si eres cliente nuevo.\n"
            "- Acceder como invitado para explorar las tapas sin registrarte.\n\n"
            "Asegúrate de que el rol seleccionado coincida con el registrado."
        )
