from PyQt5.QtWidgets import (
    QDialog, QDesktopWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QMessageBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import os

from vistas.registro import Ui_contenedorCentral
from vistas.login_view import VentanaLogin
from controladores.controladorRegistro import ControladorRegistro


class VentanaRegistro(QDialog):
    def __init__(self, conexion, coordinador=None):
        super().__init__()
        self.ui = Ui_contenedorCentral()
        self.ui.setupUi(self)
        self.coordinador = coordinador
        self.conexion = conexion  
        self.controlador = ControladorRegistro(self.conexion)  
        
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        # ✅ Cargar logo
        ruta_logo = os.path.join("interfaces", "logoGestionTapas.jpg")
        if os.path.exists(ruta_logo):
            pixmap = QPixmap(ruta_logo)
            self.ui.logo.setPixmap(pixmap.scaled(250, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.ui.logo.setAlignment(Qt.AlignCenter)

        # ✅ Estilo (opcional)
        ruta_estilo = os.path.join("estilos", "estilo.qss")
        if os.path.exists(ruta_estilo):
            with open(ruta_estilo, "r") as f:
                self.setStyleSheet(f.read())

        # ✅ Ajustar ComboBox (solo cliente)
        self.ui.comboRol.clear()
        self.ui.comboRol.addItem("cliente")
        self.ui.comboRol.setEnabled(False)

        # ✅ Conexiones de botones
        self.ui.btnRegistrarse.clicked.connect(self.intentar_registro)
        self.ui.btnCancelar.clicked.connect(self.volver_al_login)

        # ✅ Botón de ayuda
        ayuda_layout = QHBoxLayout()
        ayuda_layout.setAlignment(Qt.AlignRight)
        boton_ayuda = QPushButton("?")
        boton_ayuda.setFixedSize(30, 30)
        boton_ayuda.setToolTip("Ayuda sobre el registro")
        boton_ayuda.clicked.connect(self.mostrar_ayuda)
        ayuda_layout.addWidget(boton_ayuda)
        self.ui.verticalLayout_2.addLayout(ayuda_layout)

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

    def volver_al_login(self):
        self.close()
        self.login = VentanaLogin(self.coordinador)
        self.login.show()

    def intentar_registro(self):
        nombre = self.ui.txtNombre.text()
        email = self.ui.txtEmail.text()
        contrasena = self.ui.txtContrasena.text()
        confirmar = self.ui.txtContrasena2.text()

        mensaje_error = self.controlador.registrar_usuario(nombre, email, contrasena, confirmar)

        if mensaje_error:
            self.ui.lblError.setText(mensaje_error)
        else:
            self.ui.lblError.setText("✅ Usuario registrado correctamente.")
            # Limpiar campos tras registro exitoso
            self.ui.txtNombre.clear()
            self.ui.txtEmail.clear()
            self.ui.txtContrasena.clear()
            self.ui.txtContrasena2.clear()
