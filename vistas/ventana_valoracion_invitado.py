from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QComboBox, QSpinBox, QTextEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QFont
from modelos.dao.valoracionDAO import ValoracionDAO
from modelos.vo.valoracionVO import ValoracionVO

class VentanaValoracionInvitado(QWidget):
    tapas_pedidas = []  # Lista de tapas que el invitado pidió en esta sesión

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Valorar Tapas (Invitado)")
        self.setFixedSize(400, 300)

        with open("estilos/estilo.qss", "r") as f:
            self.setStyleSheet(f.read())

        layout = QVBoxLayout()

        titulo = QLabel("Valora la tapa que has pedido")
        titulo.setFont(QFont("Arial", 14))
        layout.addWidget(titulo)

        self.comboTapas = QComboBox()
        layout.addWidget(QLabel("Tapa:"))
        layout.addWidget(self.comboTapas)

        self.spinPuntuacion = QSpinBox()
        self.spinPuntuacion.setMinimum(1)
        self.spinPuntuacion.setMaximum(5)
        layout.addWidget(QLabel("Puntuación (1 a 5):"))
        layout.addWidget(self.spinPuntuacion)

        self.textoComentario = QTextEdit()
        layout.addWidget(QLabel("Comentario (opcional):"))
        layout.addWidget(self.textoComentario)

        self.btnEnviar = QPushButton("Enviar valoración")
        self.btnEnviar.clicked.connect(self.enviar_valoracion)
        layout.addWidget(self.btnEnviar)

        self.setLayout(layout)
        self.cargar_tapas_disponibles()

        self.valoracionDAO = ValoracionDAO()

    def cargar_tapas_disponibles(self):
        self.comboTapas.clear()
        if not VentanaValoracionInvitado.tapas_pedidas:
            self.comboTapas.addItem("No hay tapas para valorar", None)
            self.comboTapas.setEnabled(False)
        else:
            for id_tapa, nombre in VentanaValoracionInvitado.tapas_pedidas:
                self.comboTapas.addItem(nombre, id_tapa)
            self.comboTapas.setEnabled(True)

    def enviar_valoracion(self):
        id_tapa = self.comboTapas.currentData()
        puntuacion = self.spinPuntuacion.value()
        comentario = self.textoComentario.toPlainText()

        if id_tapa is None:
            QMessageBox.warning(self, "Error", "No hay tapas para valorar.")
            return

        valoracion = ValoracionVO(None, id_tapa, puntuacion, comentario)
        exito = self.valoracionDAO.insertar_valoracion(valoracion)

        if exito:
            QMessageBox.information(self, "Gracias", "Tu valoración se ha enviado.")
            self.close()
        else:
            QMessageBox.critical(self, "Error", "No se pudo enviar la valoración.")
