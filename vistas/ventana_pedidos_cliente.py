from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QFont
from modelos.dao.pedidoDAO import PedidoDAO

class VentanaPedidosCliente(QWidget):
    def __init__(self, usuario_id):
        super().__init__()
        self.setWindowTitle("Tus pedidos")
        self.setMinimumSize(500, 300)

        self.usuario_id = usuario_id
        self.pedidoDAO = PedidoDAO()

        layout = QVBoxLayout()
        self.setLayout(layout)

        titulo = QLabel("Historial de Pedidos")
        titulo.setFont(QFont("Arial", 16))
        layout.addWidget(titulo)

        self.tabla = QTableWidget()
        layout.addWidget(self.tabla)

        self.cargar_pedidos()

    def cargar_pedidos(self):
        pedidos = self.pedidoDAO.obtener_pedidos_por_usuario(self.usuario_id)

        self.tabla.setRowCount(len(pedidos))
        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels(["Tapa", "Cantidad", "Estado", "Fecha"])

        for i, (id, nombre, cantidad, estado, fecha) in enumerate(pedidos):
            self.tabla.setItem(i, 0, QTableWidgetItem(nombre))
            self.tabla.setItem(i, 1, QTableWidgetItem(str(cantidad)))
            self.tabla.setItem(i, 2, QTableWidgetItem(estado))
            self.tabla.setItem(i, 3, QTableWidgetItem(str(fecha)))
