from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QComboBox, QPushButton, QSpinBox, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modelos.dao.tapaDAO import TapaDAO 
from modelos.dao.pedidoDAO import PedidoDAO
from modelos.vo.pedidoVO import PedidoVO
from vistas.ventana_pedidos_cliente import VentanaPedidosCliente
from vistas.ventana_valoracion import VentanaValoracion

class VentanaClienteRegistrado(QWidget):
    def __init__(self, usuario_id, nombre):
        super().__init__()
        self.setWindowTitle("Panel Cliente Registrado")
        self.setFixedSize(400, 300)
        self.usuario_id = usuario_id
        self.nombre = nombre
        layout = QVBoxLayout()

        mensaje = QLabel(f"Bienvenido, {self.nombre}")
        mensaje.setAlignment(Qt.AlignCenter)
        mensaje.setFont(QFont("Arial", 16))
        layout.addWidget(mensaje)

        # ComboBox para tapas
        self.comboTapas = QComboBox()
        layout.addWidget(self.comboTapas)

        # SpinBox para cantidad
        self.spinCantidad = QSpinBox()
        self.spinCantidad.setMinimum(1)
        self.spinCantidad.setMaximum(10)
        layout.addWidget(self.spinCantidad)

        # Botón para hacer pedido
        self.btnHacerPedido = QPushButton("Hacer pedido")
        layout.addWidget(self.btnHacerPedido)

        # Botón ver pedidos
        self.btnVerPedidos = QPushButton("Ver mis pedidos")
        layout.addWidget(self.btnVerPedidos)
        self.btnVerPedidos.clicked.connect(self.abrir_historial)
        
        self.setLayout(layout)

        # Cargar las tapas desde la base de datos
        self.tapaDAO = TapaDAO()
        self.cargar_tapas()
        
        self.pedidoDAO = PedidoDAO()
        self.btnHacerPedido.clicked.connect(self.hacer_pedido)

        # Boton valoraciones
        self.btnValorar = QPushButton("Valorar tapas")
        layout.addWidget(self.btnValorar)
        self.btnValorar.clicked.connect(self.abrir_valoracion)

    def cargar_tapas(self):
        tapas = self.tapaDAO.obtener_todas_las_tapas()
        self.comboTapas.clear()
        self.comboTapas.addItem("Selecciona una tapa", None)

        for id_tapa, nombre, precio in tapas:
            texto = f"{nombre} ({float(precio):.2f}€)"
            self.comboTapas.addItem(texto, id_tapa)
            
    def hacer_pedido(self):
        id_tapa = self.comboTapas.currentData()
        cantidad = self.spinCantidad.value()

        if not id_tapa:
            QMessageBox.warning(self, "Error", "Debes seleccionar una tapa.")
            return

        pedido = PedidoVO(self.usuario_id, id_tapa, cantidad)
        exito = self.pedidoDAO.insertar_pedido(pedido)

        if exito:
            QMessageBox.information(self, "Pedido realizado", "Tu pedido ha sido registrado correctamente.")
        else:
            QMessageBox.critical(self, "Error", "No se pudo registrar el pedido.")

    def abrir_historial(self):
        self.ventana_historial = VentanaPedidosCliente(self.usuario_id)
        self.ventana_historial.show()
        
    def abrir_valoracion(self):
        self.ventana_valoracion = VentanaValoracion(self.usuario_id)
        self.ventana_valoracion.show()

