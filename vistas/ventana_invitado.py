from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
class VentanaInvitado(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Explorar como Invitado")
        self.setFixedSize(400, 200)

        layout = QVBoxLayout()
        mensaje = QLabel("Bienvenido, invitado")
        mensaje.setAlignment(Qt.AlignCenter)
        mensaje.setFont(QFont("Arial", 16))
        layout.addWidget(mensaje)

        self.setLayout(layout)
