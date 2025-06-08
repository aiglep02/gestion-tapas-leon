from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from estrategias.EstadisticaTopTapas import EstadisticaTopTapas
from controladores.controladorEstadisticas import ControladorEstadisticas
from estrategias.EstadisticaTopValoradas import EstadisticaTopValoradas


class VentanaAdmin(QWidget):
    def __init__(self,nombre_admin):
        super().__init__()
        self.nombre_admin = nombre_admin
        self.setWindowTitle("Panel Administrador")
        self.setMinimumSize(500, 400)
        
        #Aplicar el estilo
        with open("estilos/estilo.qss", "r") as f:
            self.setStyleSheet(f.read())

        layout = QVBoxLayout()
        mensaje = QLabel(f"Bienvenido, {self.nombre_admin}")
        mensaje.setAlignment(Qt.AlignCenter)
        mensaje.setFont(QFont("Arial", 16))
        layout.addWidget(mensaje)
        
        # Ver tapas más pedidas
        self.btnEstadisticas = QPushButton("Ver tapas más pedidas")
        self.btnEstadisticas.clicked.connect(self.mostrar_estadisticas)
        layout.addWidget(self.btnEstadisticas)

        # Ver tapas mejor valoradas
        self.btnVerValoradas = QPushButton("Ver tapas mejor valoradas")
        self.btnVerValoradas.clicked.connect(self.mostrar_valoradas)
        layout.addWidget(self.btnVerValoradas)

        self.tabla = QTableWidget()
        layout.addWidget(self.tabla)

        self.setLayout(layout)

    # Al hacer clic en "Ver tapas más pedidas"
    def mostrar_estadisticas(self):
        controlador = ControladorEstadisticas()
        controlador.set_estrategia(EstadisticaTopTapas())  
        resultados = controlador.calcular_estadisticas()

        self.tabla.setRowCount(len(resultados))
        self.tabla.setColumnCount(2)
        self.tabla.setHorizontalHeaderLabels(["Tapa", "Total Pedidos"])

        for i, fila in enumerate(resultados):
            self.tabla.setItem(i, 0, QTableWidgetItem(fila["nombre"]))
            self.tabla.setItem(i, 1, QTableWidgetItem(str(fila["total_pedida"])))
     
    # Al hacer clic en "Ver tapas mejor valoradas"    
    def mostrar_valoradas(self):
        controlador = ControladorEstadisticas()
        controlador.set_estrategia(EstadisticaTopValoradas()) 
        resultados = controlador.calcular_estadisticas()

        self.tabla.setRowCount(len(resultados))
        self.tabla.setColumnCount(2)
        self.tabla.setHorizontalHeaderLabels(["Tapa", "Puntuación Media"])

        for i, fila in enumerate(resultados):
            self.tabla.setItem(i, 0, QTableWidgetItem(fila["nombre"]))
            self.tabla.setItem(i, 1, QTableWidgetItem(str(fila["puntuacion_media"])))

