from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem
from estrategias.EstadisticaTopTapas import EstadisticaTopTapas
from estrategias.EstadisticaTopValoradas import EstadisticaTopValoradas
from controladores.ControladorEstadisticas import ControladorEstadisticas

class VentanaEstadisticas(QDialog):
    def __init__(self, tipo, modo="admin"):
        super().__init__()
        self.setWindowTitle("Estadísticas")
        self.setMinimumSize(400, 300)
        
        # Estilo visual
        with open("estilos/estilo.qss", "r") as f:
            self.setStyleSheet(f.read())

        layout = QVBoxLayout()
        self.tabla = QTableWidget()
        layout.addWidget(self.tabla)
        self.setLayout(layout)

        self.controlador = ControladorEstadisticas()

        if tipo == "mas_vendidas":
            self.controlador.set_estrategia(EstadisticaTopTapas())
            self.setWindowTitle("Tapas más vendidas")
            datos = self.controlador.calcular_estadisticas()

            if modo == "usuario":
                columnas = ["Tapa"]
                self.tabla.setRowCount(len(datos))
                self.tabla.setColumnCount(1)
                self.tabla.setHorizontalHeaderLabels(columnas)

                for i, fila in enumerate(datos):
                    self.tabla.setItem(i, 0, QTableWidgetItem(fila["nombre"]))
            else:
                columnas = ["Tapa", "Total Pedidos"]
                self.tabla.setRowCount(len(datos))
                self.tabla.setColumnCount(2)
                self.tabla.setHorizontalHeaderLabels(columnas)

                for i, fila in enumerate(datos):
                    self.tabla.setItem(i, 0, QTableWidgetItem(fila["nombre"]))
                    self.tabla.setItem(i, 1, QTableWidgetItem(str(fila["total_pedida"])))

        elif tipo == "mejor_valoradas":
            self.controlador.set_estrategia(EstadisticaTopValoradas())
            self.setWindowTitle("Tapas mejor valoradas")
            columnas = ["Tapa", "Puntuación Media"]
            datos = self.controlador.calcular_estadisticas()
            self.tabla.setRowCount(len(datos))
            self.tabla.setColumnCount(2)
            self.tabla.setHorizontalHeaderLabels(columnas)

            for i, fila in enumerate(datos):
                self.tabla.setItem(i, 0, QTableWidgetItem(fila["nombre"]))
                self.tabla.setItem(i, 1, QTableWidgetItem(str(fila["puntuacion_media"])))
