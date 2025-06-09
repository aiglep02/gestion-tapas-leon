from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QComboBox, QMessageBox, QHBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit
from controladores.ControladorCrearUsuario import ControladorCrearUsuario

class VentanaCrearUsuario(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Crear nuevo usuario")
        self.setFixedSize(300, 250)

        with open("estilos/estilo.qss", "r") as f:
            self.setStyleSheet(f.read())

        self.controlador = ControladorCrearUsuario()

        layout = QVBoxLayout()

        # Botón de ayuda
        ayuda_layout = QHBoxLayout()
        ayuda_layout.setAlignment(Qt.AlignRight)
        btn_ayuda = QPushButton("?")
        btn_ayuda.setFixedSize(30, 30)
        btn_ayuda.setToolTip("Ayuda sobre esta pantalla")
        btn_ayuda.clicked.connect(self.mostrar_ayuda)
        ayuda_layout.addWidget(btn_ayuda)
        layout.addLayout(ayuda_layout)

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

    def mostrar_ayuda(self):
        QMessageBox.information(
            self,
            "Ayuda - Crear Usuario",
            "Desde esta ventana puedes crear manualmente un nuevo usuario.\n\n"
            "Debes indicar:\n"
            "- Nombre: Identificador único del usuario.\n"
            "- Email: Debe ser válido.\n"
            "- Contraseña: Se almacenará de forma segura.\n"
            "- Rol: cliente, empleado o administrador.\n\n"
            "💡 Los empleados y administradores deben ser creados solo por un administrador."
        )

    def crear_usuario(self):
        nombre = self.inputNombre.text().strip()
        email = self.inputEmail.text().strip()
        contrasena = self.inputContrasena.text().strip()
        rol = self.comboRol.currentText()

        if not nombre or not email or not contrasena:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return

        resultado = self.controlador.crear_usuario(nombre, email, contrasena, rol)

        if resultado is None:
            QMessageBox.information(self, "Éxito", "Usuario creado correctamente.")
            self.inputNombre.clear()
            self.inputEmail.clear()
            self.inputContrasena.clear()
        else:
            QMessageBox.critical(self, "Error", f"No se pudo crear el usuario:\n{resultado}")
