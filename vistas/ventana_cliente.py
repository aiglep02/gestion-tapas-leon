from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class VentanaClienteRegistrado(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Panel Cliente Registrado")
        self.setFixedSize(400, 200)

        layout = QVBoxLayout()
        mensaje = QLabel("Bienvenido, Cliente Registrado")
        mensaje.setAlignment(Qt.AlignCenter)
        mensaje.setFont(QFont("Arial", 16))

        layout.addWidget(mensaje)
        self.setLayout(layout)
