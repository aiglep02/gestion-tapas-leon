from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QSpinBox,
    QTextEdit, QPushButton, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from modelos.dao.pedidoDAO import PedidoDAO
from modelos.dao.valoracionDAO import ValoracionDAO
from modelos.vo.valoracionVO import ValoracionVO

class VentanaValoracion(QWidget):
    def __init__(self, usuario_id):
        super().__init__()
        self.usuario_id = usuario_id
        self.setWindowTitle("Valorar Tapas")
        self.setMinimumSize(500, 300)

        self.pedidoDAO = PedidoDAO()
        self.valoracionDAO = ValoracionDAO()
        
        with open("estilos/estilo.qss", "r") as f:
            self.setStyleSheet(f.read())

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Botón de ayuda
        ayuda_layout = QHBoxLayout()
        ayuda_layout.setAlignment(Qt.AlignRight)
        boton_ayuda = QPushButton("?")
        boton_ayuda.setFixedSize(30, 30)
        boton_ayuda.setToolTip("Ayuda sobre esta pantalla")
        boton_ayuda.clicked.connect(self.mostrar_ayuda)
        ayuda_layout.addWidget(boton_ayuda)
        layout.addLayout(ayuda_layout)

        titulo = QLabel("Valora tus tapas entregadas")
        titulo.setFont(QFont("Arial", 16))
        layout.addWidget(titulo)

        self.comboTapas = QComboBox()
        layout.addWidget(QLabel("Tapa entregada:"))
        layout.addWidget(self.comboTapas)

        self.spinPuntuacion = QSpinBox()
        self.spinPuntuacion.setMinimum(1)
        self.spinPuntuacion.setMaximum(5)
        layout.addWidget(QLabel("Puntuación (1 a 5):"))
        layout.addWidget(self.spinPuntuacion)

        self.textoComentario = QTextEdit()
        layout.addWidget(QLabel("Comentario:"))
        layout.addWidget(self.textoComentario)

        self.btnEnviar = QPushButton("Enviar valoración")
        layout.addWidget(self.btnEnviar)

        self.btnEnviar.clicked.connect(self.enviar_valoracion)

        self.cargar_tapas_entregadas()

    def mostrar_ayuda(self):
        QMessageBox.information(
            self,
            "Ayuda - Valoración de Tapas",
            "En esta pantalla puedes valorar tapas que ya has recibido.\n\n"
            "Selecciona una tapa que haya sido entregada, asigna una puntuación del 1 al 5\n"
            "y añade un comentario si lo deseas. Tu opinión ayudará a mejorar el servicio."
        )

    def cargar_tapas_entregadas(self):
        pedidos = self.pedidoDAO.obtener_pedidos_entregados_por_usuario(self.usuario_id)
        self.comboTapas.clear()
        for id_tapa, nombre in pedidos:
            self.comboTapas.addItem(nombre, id_tapa)

    def enviar_valoracion(self):
        id_tapa = self.comboTapas.currentData()
        puntuacion = self.spinPuntuacion.value()
        comentario = self.textoComentario.toPlainText()

        if not id_tapa:
            QMessageBox.warning(self, "Error", "Debes seleccionar una tapa.")
            return

        valoracion = ValoracionVO(self.usuario_id, id_tapa, puntuacion, comentario)
        exito = self.valoracionDAO.insertar_valoracion(valoracion)

        if exito:
            QMessageBox.information(self, "Gracias", "Valoración enviada correctamente.")
            self.close()
        else:
            QMessageBox.critical(self, "Error", "No se pudo enviar la valoración.")
