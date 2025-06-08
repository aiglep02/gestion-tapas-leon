from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QHeaderView, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modelos.dao.pedidoDAO import PedidoDAO
from modelos.dao.tapaDAO import TapaDAO

class VentanaEmpleado(QWidget):
    def __init__(self, nombre_empleado, coordinador):
        super().__init__()
        self.setWindowTitle("Panel de Empleado")
        self.setMinimumSize(900, 400)
        self.nombre_empleado = nombre_empleado
        self.pedidoDAO = PedidoDAO()
        self.tapaDAO = TapaDAO()
        self.coordinador = coordinador

        with open("estilos/estilo.qss", "r") as f:
            self.setStyleSheet(f.read())

        layout = QVBoxLayout()

        # Botón cerrar sesión
        self.btnCerrarSesion = QPushButton("Cerrar sesión")
        self.btnCerrarSesion.clicked.connect(self.cerrar_sesion)
        layout.addWidget(self.btnCerrarSesion)

        # Botón ayuda
        ayuda_layout = QHBoxLayout()
        ayuda_layout.setAlignment(Qt.AlignRight)
        boton_ayuda = QPushButton("?")
        boton_ayuda.setFixedSize(30, 30)
        boton_ayuda.clicked.connect(self.mostrar_ayuda)
        ayuda_layout.addWidget(boton_ayuda)
        layout.addLayout(ayuda_layout)

        # Mensaje bienvenida
        mensaje = QLabel(f"Bienvenido, {self.nombre_empleado}")
        mensaje.setAlignment(Qt.AlignCenter)
        mensaje.setFont(QFont("Arial", 16))
        layout.addWidget(mensaje)

        self.tabla = QTableWidget()
        layout.addWidget(self.tabla)

        self.setLayout(layout)
        self.cargar_pedidos()

    def cerrar_sesion(self):
        self.close()
        from vistas.login_view import VentanaLogin
        self.login = VentanaLogin(self.coordinador)
        self.login.show()

    def mostrar_ayuda(self):
        QMessageBox.information(
            self,
            "Ayuda - Panel Empleado",
            "Desde esta pantalla puedes gestionar los pedidos realizados por los clientes:\n"
            "- Preparar, marcar como listo o entregado.\n"
            "- Cada entrega resta del stock disponible.\n"
            "- Solo verás pedidos en estado pendiente, preparación o listo.\n"
            "Revisa la tabla para ver el estado y actuar sobre ellos."
        )

    def cargar_pedidos(self):
        pedidos = self.pedidoDAO.obtener_pedidos_pendientes()
        self.tabla.setRowCount(len(pedidos))
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels(["Cliente", "Tapa", "Cantidad", "Estado", "Fecha", "Acciones"])

        self.tabla.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tabla.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tabla.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.tabla.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.tabla.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.tabla.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.tabla.setColumnWidth(5, 220)

        for i, (id_pedido, cliente, tapa, cantidad, estado, fecha) in enumerate(pedidos):
            self.tabla.setItem(i, 0, QTableWidgetItem(cliente))
            self.tabla.setItem(i, 1, QTableWidgetItem(tapa))
            self.tabla.setItem(i, 2, QTableWidgetItem(str(cantidad)))
            self.tabla.setItem(i, 3, QTableWidgetItem(estado))
            self.tabla.setItem(i, 4, QTableWidgetItem(str(fecha)))

            acciones_widget = QWidget()
            acciones_layout = QHBoxLayout()

            btn_preparar = QPushButton("Preparar")
            btn_preparar.clicked.connect(lambda _, pid=id_pedido: self.actualizar_estado(pid, "en preparación"))

            btn_listo = QPushButton("Listo")
            btn_listo.clicked.connect(lambda _, pid=id_pedido: self.actualizar_estado(pid, "listo"))

            btn_entregado = QPushButton("Entregado")
            btn_entregado.clicked.connect(lambda _, pid=id_pedido, nombre=tapa, cant=cantidad: self.entregar_pedido(pid, nombre, cant))

            for btn in (btn_preparar, btn_listo, btn_entregado):
                btn.setMinimumWidth(60)
                acciones_layout.addWidget(btn)

            acciones_layout.setSpacing(6)
            acciones_layout.setContentsMargins(0, 0, 0, 0)
            acciones_widget.setLayout(acciones_layout)
            self.tabla.setCellWidget(i, 5, acciones_widget)

    def actualizar_estado(self, id_pedido, nuevo_estado):
        exito = self.pedidoDAO.actualizar_estado_pedido(id_pedido, nuevo_estado)
        if exito:
            self.cargar_pedidos()

    def entregar_pedido(self, id_pedido, nombre_tapa, cantidad):
        exito = self.pedidoDAO.actualizar_estado_pedido(id_pedido, "entregado")
        if exito:
            self.tapaDAO.reducir_stock_por_nombre(nombre_tapa, cantidad)
            self.cargar_pedidos()
