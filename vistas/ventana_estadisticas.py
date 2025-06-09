from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QMessageBox, QHBoxLayout
)
from estrategias.EstadisticaTopTapas import EstadisticaTopTapas
from estrategias.EstadisticaTopValoradas import EstadisticaTopValoradas
from controladores.ControladorEstadisticas import ControladorEstadisticas
from PyQt5.QtCore import Qt

class VentanaEstadisticas(QDialog):
    def __init__(self, tipo, modo="admin"):
        super().__init__()
        self.setMinimumSize(400, 300)
        self.tipo = tipo
        self.modo = modo
        self.setWindowTitle("Estadísticas")

        # Estilo visual
        with open("estilos/estilo.qss", "r") as f:
            self.setStyleSheet(f.read())

        # Layout principal
        layout = QVBoxLayout()

        # Layout para botón de ayuda
        ayuda_layout = QHBoxLayout()
        ayuda_layout.setAlignment(Qt.AlignRight)
        boton_ayuda = QPushButton("?")
        boton_ayuda.setFixedSize(30, 30)
        boton_ayuda.setToolTip("Ayuda sobre estadísticas")
        boton_ayuda.clicked.connect(self.mostrar_ayuda)
        ayuda_layout.addWidget(boton_ayuda)
        layout.addLayout(ayuda_layout)

        self.tabla = QTableWidget()
        layout.addWidget(self.tabla)
        self.setLayout(layout)

        # Controlador y estrategia
        self.controlador = ControladorEstadisticas()

        if tipo == "mas_vendidas":
            self.setWindowTitle("Tapas más vendidas")
            self.controlador.set_estrategia(EstadisticaTopTapas())
            datos = self.controlador.calcular_estadisticas()

            if modo == "usuario":
                columnas = ["Tapa"]
                self.tabla.setColumnCount(1)
                self.tabla.setHorizontalHeaderLabels(columnas)
                self.tabla.setRowCount(len(datos))
                for i, fila in enumerate(datos):
                    self.tabla.setItem(i, 0, QTableWidgetItem(fila["nombre"]))
            else:
                columnas = ["Tapa", "Total Pedidos"]
                self.tabla.setColumnCount(2)
                self.tabla.setHorizontalHeaderLabels(columnas)
                self.tabla.setRowCount(len(datos))
                for i, fila in enumerate(datos):
                    self.tabla.setItem(i, 0, QTableWidgetItem(fila["nombre"]))
                    self.tabla.setItem(i, 1, QTableWidgetItem(str(fila["total_pedida"])))

        elif tipo == "mejor_valoradas":
            self.setWindowTitle("Tapas mejor valoradas")
            self.controlador.set_estrategia(EstadisticaTopValoradas())
            datos = self.controlador.calcular_estadisticas()
            columnas = ["Tapa", "Puntuación Media"]
            self.tabla.setColumnCount(2)
            self.tabla.setHorizontalHeaderLabels(columnas)
            self.tabla.setRowCount(len(datos))
            for i, fila in enumerate(datos):
                self.tabla.setItem(i, 0, QTableWidgetItem(fila["nombre"]))
                self.tabla.setItem(i, 1, QTableWidgetItem(str(fila["puntuacion_media"])))

    def mostrar_ayuda(self):
        if self.tipo == "mas_vendidas":
            texto = "Se muestran las tapas que han sido más solicitadas por los clientes."
        elif self.tipo == "mejor_valoradas":
            texto = "Se muestran las tapas con mejor puntuación media según las valoraciones recibidas."
        else:
            texto = "Pantalla de estadísticas de tapas."

        QMessageBox.information(
            self,
            "Ayuda - Estadísticas",
            texto
        )