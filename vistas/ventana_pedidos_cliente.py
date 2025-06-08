from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from modelos.dao.pedidoDAO import PedidoDAO

class VentanaPedidosCliente(QWidget):
    def __init__(self, usuario_id):
        super().__init__()
        self.setWindowTitle("Pedidos del Cliente")
        self.setFixedSize(600, 400)
        self.usuario_id = usuario_id
        
        # Aplicar estilo visual desde estilo.qss
        with open("estilos/estilo.qss", "r") as f:
            self.setStyleSheet(f.read())
        
        layout = QVBoxLayout()

        mensaje = QLabel(f"Pedidos de {self.usuario_id}")
        mensaje.setAlignment(Qt.AlignCenter)
        mensaje.setFont(QFont("Arial", 16))
        layout.addWidget(mensaje)

        self.tabla = QTableWidget()
        layout.addWidget(self.tabla)

        self.setLayout(layout)

        # Cargar los pedidos del cliente
        self.pedidoDAO = PedidoDAO()
        self.cargar_pedidos()

    def cargar_pedidos(self):
        pedidos = self.pedidoDAO.obtener_pedidos_por_usuario(self.usuario_id)

        self.tabla.setRowCount(len(pedidos))
        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels(["ID", "Tapa", "Cantidad", "Estado"])

        for i, (id_pedido, tapa, cantidad, estado) in enumerate(pedidos):
            self.tabla.setItem(i, 0, QTableWidgetItem(str(id_pedido)))
            self.tabla.setItem(i, 1, QTableWidgetItem(tapa))
            self.tabla.setItem(i, 2, QTableWidgetItem(str(cantidad)))
            self.tabla.setItem(i, 3, QTableWidgetItem(estado))
