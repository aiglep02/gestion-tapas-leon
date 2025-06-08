from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QHeaderView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modelos.dao.pedidoDAO import PedidoDAO

class VentanaEmpleado(QWidget):
    def __init__(self, nombre_empleado, coordinador):
        super().__init__()
        self.setWindowTitle("Panel de Empleado")
        self.setMinimumSize(900, 400)
        self.nombre_empleado = nombre_empleado
        self.pedidoDAO = PedidoDAO()
        self.coordinador = coordinador

        # Aplicar estilo visual desde estilo.qss
        with open("estilos/estilo.qss", "r") as f:
            self.setStyleSheet(f.read())

        layout = QVBoxLayout()

        self.btnCerrarSesion = QPushButton("Cerrar sesión")
        self.btnCerrarSesion.clicked.connect(self.cerrar_sesion)
        layout.addWidget(self.btnCerrarSesion)


        mensaje = QLabel(f"Bienvenido, {self.nombre_empleado}")
        mensaje.setAlignment(Qt.AlignCenter)
        mensaje.setFont(QFont("Arial", 16))
        layout.addWidget(mensaje)

        self.tabla = QTableWidget()
        layout.addWidget(self.tabla)

        self.setLayout(layout)
        self.cargar_pedidos()

    #Botón cerrar sesión
    def cerrar_sesion(self):
        self.close()
        from vistas.login_view import VentanaLogin
        self.login = VentanaLogin(self.coordinador)
        self.login.show()

    
    def cargar_pedidos(self):
        pedidos = self.pedidoDAO.obtener_pedidos_pendientes()

        self.tabla.setRowCount(len(pedidos))
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels(["Cliente", "Tapa", "Cantidad", "Estado", "Fecha", "Acciones"])

        # Ajustar tamaño de columnas
        self.tabla.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.tabla.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tabla.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.tabla.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.tabla.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.tabla.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.tabla.setColumnWidth(5, 220)  # ✅ Espacio suficiente para 3 botones

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
            btn_preparar.setObjectName("btnPreparar")
            btn_preparar.clicked.connect(lambda _, pid=id_pedido: self.actualizar_estado(pid, "en preparación"))

            btn_listo = QPushButton("Listo")
            btn_listo.setObjectName("btnListo")
            btn_listo.clicked.connect(lambda _, pid=id_pedido: self.actualizar_estado(pid, "listo"))

            btn_entregado = QPushButton("Entregado")
            btn_entregado.setObjectName("btnEntregado")
            btn_entregado.clicked.connect(lambda _, pid=id_pedido: self.actualizar_estado(pid, "entregado"))

            for btn in (btn_preparar, btn_listo, btn_entregado):
                btn.setMinimumWidth(60)  # Opcional: para asegurar tamaño consistente
                acciones_layout.addWidget(btn)

            acciones_layout.setSpacing(6)
            acciones_layout.setContentsMargins(0, 0, 0, 0)
            acciones_widget.setLayout(acciones_layout)
            self.tabla.setCellWidget(i, 5, acciones_widget)

    def actualizar_estado(self, id_pedido, nuevo_estado):
        exito = self.pedidoDAO.actualizar_estado_pedido(id_pedido, nuevo_estado)
        if exito:
            self.cargar_pedidos()