from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QComboBox, QPushButton, QHBoxLayout, QMessageBox, QHeaderView
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from modelos.dao.pedidoDAO import PedidoDAO
from modelos.dao.tapaDAO import TapaDAO

class VentanaPedidosCliente(QWidget):
    def __init__(self, usuario_id):
        super().__init__()
        self.setWindowTitle("Pedidos del Cliente")
        self.setFixedSize(700, 400)
        self.usuario_id = usuario_id

        with open("estilos/estilo.qss", "r") as f:
            self.setStyleSheet(f.read())

        layout = QVBoxLayout()

        mensaje = QLabel("Mis pedidos")
        mensaje.setAlignment(Qt.AlignCenter)
        mensaje.setFont(QFont("Arial", 16))
        layout.addWidget(mensaje)

        self.tabla = QTableWidget()
        layout.addWidget(self.tabla)

        self.setLayout(layout)

        self.pedidoDAO = PedidoDAO()
        self.tapaDAO = TapaDAO()
        self.cargar_pedidos()

    def cargar_pedidos(self):
        pedidos = self.pedidoDAO.obtener_pedidos_por_usuario(self.usuario_id)

        self.tabla.clearContents()        # Limpia contenido anterior (widgets incluidos)
        self.tabla.setRowCount(0)         # Elimina filas viejas
        self.tabla.setRowCount(len(pedidos))
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(["ID", "Tapa", "Cantidad", "Estado", "Acciones"])

        # Ajuste de columnas
        self.tabla.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)  # ID
        self.tabla.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)           # Tapa
        self.tabla.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Cantidad
        self.tabla.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Estado
        self.tabla.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Acciones
        self.tabla.setColumnWidth(4, 260)

        for i, (id_pedido, tapa, cantidad, estado) in enumerate(pedidos):
            self.tabla.setItem(i, 0, QTableWidgetItem(str(id_pedido)))
            self.tabla.setItem(i, 1, QTableWidgetItem(tapa))
            self.tabla.setItem(i, 2, QTableWidgetItem(str(cantidad)))
            self.tabla.setItem(i, 3, QTableWidgetItem(estado))

            if estado == "en preparación":
                acciones = QWidget()
                layout = QHBoxLayout()
                layout.setContentsMargins(0, 0, 0, 0)
                layout.setSpacing(4)

                combo = QComboBox()
                tapas = self.tapaDAO.obtener_todas_las_tapas()
                for id_tapa, nombre, precio in tapas:
                    combo.addItem(f"{nombre} ({precio}€)", id_tapa)
                layout.addWidget(combo)

                btn_cambiar = QPushButton("Cambiar")
                btn_cambiar.setMinimumWidth(70)
                btn_cambiar.clicked.connect(lambda _, pid=id_pedido, cb=combo: self.cambiar_tapa(pid, cb))
                layout.addWidget(btn_cambiar)

                btn_eliminar = QPushButton("Eliminar")
                btn_eliminar.setMinimumWidth(70)
                btn_eliminar.clicked.connect(lambda _, pid=id_pedido: self.eliminar_pedido(pid))
                layout.addWidget(btn_eliminar)

                acciones.setLayout(layout)
                self.tabla.setCellWidget(i, 4, acciones)
            else:
                self.tabla.setItem(i, 4, QTableWidgetItem("-"))


    def eliminar_pedido(self, pedido_id):
        confirm = QMessageBox.question(
            self,
            "Eliminar pedido",
            "¿Estás seguro de que quieres eliminar este pedido?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            eliminado = self.pedidoDAO.eliminar_pedido(pedido_id)
            if eliminado:
                QMessageBox.information(self, "Eliminado", "El pedido ha sido eliminado correctamente.")
                self.cargar_pedidos()
            else:
                QMessageBox.warning(self, "Error", "No se pudo eliminar el pedido.")

                                
    def cambiar_tapa(self, pedido_id, combo):
        nueva_tapa_id = combo.currentData()
        if nueva_tapa_id:
            actualizado = self.pedidoDAO.actualizar_tapa_pedido(pedido_id, nueva_tapa_id)
            if actualizado:
                QMessageBox.information(self, "Tapa cambiada", "El pedido ha sido actualizado.")
                self.cargar_pedidos()
            else:
                QMessageBox.warning(self, "Error", "No se pudo actualizar la tapa.")
