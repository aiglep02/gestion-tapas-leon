from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QWidget, QHeaderView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modelos.dao.pedidoDAO import PedidoDAO

class VentanaEmpleado(QWidget):
    def __init__(self, nombre_empleado):
        super().__init__()
        self.setWindowTitle("Panel de Empleado")
        self.setMinimumSize(900, 400)
        self.nombre_empleado = nombre_empleado
        self.pedidoDAO = PedidoDAO()

        layout = QVBoxLayout()

        mensaje = QLabel(f"Bienvenido, {self.nombre_empleado}")
        mensaje.setAlignment(Qt.AlignCenter)
        mensaje.setFont(QFont("Arial", 16))
        layout.addWidget(mensaje)

        self.tabla = QTableWidget()
        layout.addWidget(self.tabla)

        self.setLayout(layout)

        self.cargar_pedidos()

    def cargar_pedidos(self):
        pedidos = self.pedidoDAO.obtener_pedidos_pendientes()

        self.tabla.setRowCount(len(pedidos))
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels(["Cliente", "Tapa", "Cantidad", "Estado", "Fecha", "Acciones"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Cliente
        self.tabla.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)           # Tapa
        self.tabla.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Cantidad
        self.tabla.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Estado
        self.tabla.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Fecha
        self.tabla.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Acciones


        for i, (id_pedido, cliente, tapa, cantidad, estado, fecha) in enumerate(pedidos):
            self.tabla.setItem(i, 0, QTableWidgetItem(cliente))
            self.tabla.setItem(i, 1, QTableWidgetItem(tapa))
            self.tabla.setItem(i, 2, QTableWidgetItem(str(cantidad)))
            self.tabla.setItem(i, 3, QTableWidgetItem(estado))
            self.tabla.setItem(i, 4, QTableWidgetItem(str(fecha)))

            # Botones de acción
            acciones_widget = QWidget()
            acciones_layout = QHBoxLayout()

            btn_preparar = QPushButton("Preparar")
            btn_preparar.clicked.connect(lambda _, id=id_pedido: self.actualizar_estado(id, "en preparación"))

            btn_listo = QPushButton("Listo")
            btn_listo.clicked.connect(lambda _, id=id_pedido: self.actualizar_estado(id, "listo"))

            btn_entregado = QPushButton("Entregado")
            btn_entregado.clicked.connect(lambda _, id=id_pedido: self.actualizar_estado(id, "entregado"))

            for btn in (btn_preparar, btn_listo, btn_entregado):
                acciones_layout.addWidget(btn)

            acciones_layout.setContentsMargins(0, 0, 0, 0)
            acciones_widget.setLayout(acciones_layout)
            self.tabla.setCellWidget(i, 5, acciones_widget)

    def actualizar_estado(self, id_pedido, nuevo_estado):
        exito = self.pedidoDAO.actualizar_estado_pedido(id_pedido, nuevo_estado)
        if exito:
            self.cargar_pedidos()  

