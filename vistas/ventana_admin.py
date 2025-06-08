from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QMessageBox, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class VentanaAdmin(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Panel Administrador")
        self.setFixedSize(400, 200)

        # Layout principal
        layout = QVBoxLayout()

        # Layout superior para botón de ayuda
        ayuda_layout = QHBoxLayout()
        ayuda_layout.setAlignment(Qt.AlignRight)
        boton_ayuda = QPushButton("?")
        boton_ayuda.setFixedSize(30, 30)
        boton_ayuda.setToolTip("Ayuda sobre esta pantalla")
        boton_ayuda.clicked.connect(self.mostrar_ayuda)
        ayuda_layout.addWidget(boton_ayuda)
        layout.addLayout(ayuda_layout)

        # Mensaje central
        mensaje = QLabel("Bienvenido, Administrador")
        mensaje.setAlignment(Qt.AlignCenter)
        mensaje.setFont(QFont("Arial", 16))
        layout.addWidget(mensaje)

        self.setLayout(layout)

    def mostrar_ayuda(self):
        QMessageBox.information(
            self,
            "Ayuda - Panel Administrador",
            "Desde esta pantalla puedes:\n"
            "- Gestionar tapas (crear, modificar, eliminar)\n"
            "- Consultar y gestionar usuarios\n"
            "- Visualizar estadísticas de uso del sistema"
        )
