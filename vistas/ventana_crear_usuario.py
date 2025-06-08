from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox
from controladores.ControladorUsuarios import ControladorUsuarios
from modelos.ConexionMYSQL import ConexionMYSQL
import hashlib
import os

class VentanaCrearUsuario(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Crear nuevo usuario")
        self.setFixedSize(300, 250)

        with open("estilos/estilo.qss", "r") as f:
            self.setStyleSheet(f.read())

        self.conexion = ConexionMYSQL()._conexion
        self.controlador = ControladorUsuarios(self.conexion)

        layout = QVBoxLayout()

        self.inputNombre = QLineEdit()
        self.inputNombre.setPlaceholderText("Nombre")
        layout.addWidget(self.inputNombre)

        self.inputEmail = QLineEdit()
        self.inputEmail.setPlaceholderText("Email")
        layout.addWidget(self.inputEmail)

        self.inputContrasena = QLineEdit()
        self.inputContrasena.setPlaceholderText("Contraseña")
        self.inputContrasena.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.inputContrasena)

        self.comboRol = QComboBox()
        self.comboRol.addItems(["cliente", "empleado", "administrador"])
        layout.addWidget(self.comboRol)

        self.btnCrear = QPushButton("Crear usuario")
        self.btnCrear.clicked.connect(self.crear_usuario)
        layout.addWidget(self.btnCrear)

        self.setLayout(layout)

    def crear_usuario(self):
        nombre = self.inputNombre.text().strip()
        email = self.inputEmail.text().strip()
        contrasena = self.inputContrasena.text().strip()
        rol = self.comboRol.currentText()

        if not nombre or not email or not contrasena:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return

        contrasena_hash = hashlib.sha256(contrasena.encode()).hexdigest()

        try:
            self.controlador.crear_usuario(nombre, email, contrasena_hash, rol)
            QMessageBox.information(self, "Éxito", "Usuario creado correctamente.")
            self.accept()  # cierra la ventana
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo crear el usuario:\n{e}")
