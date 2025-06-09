from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QComboBox, QSpinBox, QTextEdit,
    QPushButton, QMessageBox
)
from PyQt5.QtGui import QFont
from controladores.ControladorValoracionInvitado import ControladorValoracionInvitado

class VentanaValoracionInvitado(QWidget):
    def __init__(self, tapas_pedidas):
        super().__init__()
        self.setWindowTitle("Valorar Tapas (Invitado)")
        self.setFixedSize(400, 300)

        with open("estilos/estilo.qss", "r") as f:
            self.setStyleSheet(f.read())

        self.controlador = ControladorValoracionInvitado()
        self.tapas_pedidas = tapas_pedidas

        layout = QVBoxLayout()

        titulo = QLabel("Valora la tapa que has pedido")
        titulo.setFont(QFont("Arial", 14))
        layout.addWidget(titulo)

        layout.addWidget(QLabel("Tapa:"))
        self.comboTapas = QComboBox()
        layout.addWidget(self.comboTapas)

        layout.addWidget(QLabel("Puntuación (1 a 5):"))
        self.spinPuntuacion = QSpinBox()
        self.spinPuntuacion.setMinimum(1)
        self.spinPuntuacion.setMaximum(5)
        layout.addWidget(self.spinPuntuacion)

        layout.addWidget(QLabel("Comentario (opcional):"))
        self.textoComentario = QTextEdit()
        layout.addWidget(self.textoComentario)

        self.btnEnviar = QPushButton("Enviar valoración")
        self.btnEnviar.clicked.connect(self.enviar_valoracion)
        layout.addWidget(self.btnEnviar)

        self.setLayout(layout)
        self.cargar_tapas_disponibles()

    def cargar_tapas_disponibles(self):
        self.comboTapas.clear()
        if not self.tapas_pedidas:
            self.comboTapas.addItem("No hay tapas para valorar", None)
            self.comboTapas.setEnabled(False)
        else:
            for id_tapa, nombre in self.tapas_pedidas:
                self.comboTapas.addItem(nombre, id_tapa)
            self.comboTapas.setEnabled(True)

    def enviar_valoracion(self):
        id_tapa = self.comboTapas.currentData()
        puntuacion = self.spinPuntuacion.value()
        comentario = self.textoComentario.toPlainText()

        if id_tapa is None:
            QMessageBox.warning(self, "Error", "No hay tapas para valorar.")
            return

        exito = self.controlador.enviar_valoracion(id_tapa, puntuacion, comentario)

        if exito:
            QMessageBox.information(self, "Gracias", "Tu valoración se ha enviado.")
            self.close()
        else:
            QMessageBox.critical(self, "Error", "No se pudo enviar la valoración.")
