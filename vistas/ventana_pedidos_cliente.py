from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QComboBox, QPushButton, QHBoxLayout, QMessageBox, QHeaderView, QSizePolicy
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from controladores.ControladorPedido import ControladorPedido
from controladores.ControladorTapa import ControladorTapa

class VentanaPedidosCliente(QWidget):
    def __init__(self, usuario_id, coordinador):
        super().__init__()
        self.setWindowTitle("Pedidos del Cliente")
        self.setFixedSize(750, 400)
        self.usuario_id = usuario_id
        self.coordinador = coordinador

        with open("estilos/estilo.qss", "r") as f:
            self.setStyleSheet(f.read())

        self.controlador_pedidos = ControladorPedido()
        self.controlador_tapas = ControladorTapa()

        layout = QVBoxLayout()

        # Botón de ayuda
        ayuda_layout = QHBoxLayout()
        ayuda_layout.setAlignment(Qt.AlignRight)
        boton_ayuda = QPushButton("?")
        boton_ayuda.setFixedSize(30, 30)
        boton_ayuda.setToolTip("Ayuda sobre esta pantalla")
        boton_ayuda.clicked.connect(self.mostrar_ayuda)
        ayuda_layout.addWidget(boton_ayuda)
        layout.addLayout(ayuda_layout)

        mensaje = QLabel("Mis pedidos")
        mensaje.setAlignment(Qt.AlignCenter)
        mensaje.setFont(QFont("Arial", 16))
        layout.addWidget(mensaje)

        self.tabla = QTableWidget()
        layout.addWidget(self.tabla)

        self.setLayout(layout)
        self.cargar_pedidos()

    def mostrar_ayuda(self):
        QMessageBox.information(
            self,
            "Ayuda - Pedidos del Cliente",
            "Aquí puedes consultar tus pedidos anteriores.\n\n"
            "Si un pedido aún está 'en preparación', puedes:\n"
            " - Cambiar la tapa seleccionada por otra\n"
            " - Eliminar el pedido si lo deseas\n\n"
            "Una vez que el pedido ha sido preparado, ya no se puede modificar."
        )

    def cargar_pedidos(self):
        pedidos = self.controlador_pedidos.obtener_pedidos_usuario(self.usuario_id)
        tapas = self.controlador_tapas.obtener_tapas()

        self.tabla.clearContents()
        self.tabla.setRowCount(len(pedidos))
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(["ID", "Tapa", "Cantidad", "Estado", "Acciones"])

        # Asignar ancho personalizado a cada columna
        self.tabla.setColumnWidth(0, 50)   # ID
        self.tabla.setColumnWidth(1, 200)  # Tapa
        self.tabla.setColumnWidth(2, 70)   # Cantidad
        self.tabla.setColumnWidth(3, 130)  # Estado
        self.tabla.setColumnWidth(4, 280)  # Acciones

        for i, pedido in enumerate(pedidos):
            self.tabla.setItem(i, 0, QTableWidgetItem(str(pedido.id)))
            nombre_tapa = next((t.nombre for t in tapas if t.id_tapa == pedido.id_tapa), "Desconocida")
            self.tabla.setItem(i, 1, QTableWidgetItem(nombre_tapa))
            self.tabla.setItem(i, 2, QTableWidgetItem(str(pedido.cantidad)))
            self.tabla.setItem(i, 3, QTableWidgetItem(pedido.estado))

            if pedido.estado == "en preparación":
                acciones_widget = QWidget()
                acciones_layout = QHBoxLayout(acciones_widget)
                acciones_layout.setContentsMargins(0, 0, 0, 0)
                acciones_layout.setSpacing(6)

                combo = QComboBox()
                combo.setMinimumWidth(120)
                combo.setFixedHeight(26)
                for tapa in tapas:
                    combo.addItem(tapa.nombre, tapa.id_tapa)
                acciones_layout.addWidget(combo)

                btn_cambiar = QPushButton("Cambiar")
                btn_cambiar.setMinimumWidth(80)
                btn_cambiar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
                btn_cambiar.clicked.connect(lambda _, pid=pedido.id, cb=combo: self.cambiar_tapa(pid, cb))
                acciones_layout.addWidget(btn_cambiar)

                btn_eliminar = QPushButton("Eliminar")
                btn_eliminar.setMinimumWidth(80)
                btn_eliminar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
                btn_eliminar.clicked.connect(lambda _, pid=pedido.id: self.eliminar_pedido(pid))
                acciones_layout.addWidget(btn_eliminar)

                acciones_layout.addStretch()
                self.tabla.setCellWidget(i, 4, acciones_widget)
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
            eliminado = self.controlador_pedidos.eliminar_pedido(pedido_id)
            if eliminado:
                QMessageBox.information(self, "Eliminado", "El pedido ha sido eliminado correctamente.")
                self.cargar_pedidos()
            else:
                QMessageBox.warning(self, "Error", "No se pudo eliminar el pedido.")

    def cambiar_tapa(self, pedido_id, combo):
        nueva_tapa_id = combo.currentData()
        if nueva_tapa_id:
            actualizado = self.controlador_pedidos.cambiar_tapa_pedido(pedido_id, nueva_tapa_id)
            if actualizado:
                QMessageBox.information(self, "Tapa cambiada", "El pedido ha sido actualizado.")
                self.cargar_pedidos()
            else:
                QMessageBox.warning(self, "Error", "No se pudo actualizar la tapa.")
