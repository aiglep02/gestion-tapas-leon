from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class VentanaAdmin(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Panel Administrador")
        self.setFixedSize(400, 200)

        layout = QVBoxLayout()
        mensaje = QLabel("Bienvenido, Administrador")
        mensaje.setAlignment(Qt.AlignCenter)
        mensaje.setFont(QFont("Arial", 16))

        layout.addWidget(mensaje)
        self.setLayout(layout)
