from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QMessageBox, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class VentanaInvitado(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Explorar como Invitado")
        self.setFixedSize(400, 200)

        layout = QVBoxLayout()

        ayuda_layout = QHBoxLayout()
        ayuda_layout.setAlignment(Qt.AlignRight)
        btn_ayuda = QPushButton("?")
        btn_ayuda.setFixedSize(30, 30)
        btn_ayuda.clicked.connect(self.mostrar_ayuda)
        ayuda_layout.addWidget(btn_ayuda)
        layout.addLayout(ayuda_layout)

        mensaje = QLabel("Bienvenido, invitado")
        mensaje.setAlignment(Qt.AlignCenter)
        mensaje.setFont(QFont("Arial", 16))
        layout.addWidget(mensaje)

        self.setLayout(layout)

    def mostrar_ayuda(self):
        QMessageBox.information(
            self,
            "Ayuda - Invitado",
            "Puedes explorar la aplicación como invitado.\n"
            "Para realizar pedidos, valorar tapas o configurar preferencias,\n"
            "deberás registrarte como cliente."
        )
