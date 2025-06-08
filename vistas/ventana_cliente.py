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
from vistas.ventana_estadisticas import VentanaEstadisticas

class VentanaClienteRegistrado(QWidget):
    def __init__(self, usuario_id, nombre, coordinador):
        super().__init__()
        self.setWindowTitle("Panel Cliente Registrado")
        self.setFixedSize(400, 300)
        self.usuario_id = usuario_id
        self.nombre = nombre
        self.coordinador = coordinador

        # Estilo visual
        with open("estilos/estilo.qss", "r") as f:
            self.setStyleSheet(f.read())

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

        # Botón ver historial de pedidos
        self.btnVerPedidos = QPushButton("Ver mis pedidos")
        self.btnVerPedidos.setObjectName("btnVerPedidos")
        layout.addWidget(self.btnVerPedidos)
        self.btnVerPedidos.clicked.connect(self.abrir_historial)

        # Botón valorar tapas
        self.btnValorar = QPushButton("Valorar tapas")
        self.btnValorar.setObjectName("btnValorar")
        layout.addWidget(self.btnValorar)
        self.btnValorar.clicked.connect(self.abrir_valoracion)

        # Botón tapas más vendidas
        self.btnMasVendidas = QPushButton("Ver tapas más vendidas")
        layout.addWidget(self.btnMasVendidas)
        self.btnMasVendidas.clicked.connect(self.mostrar_mas_vendidas)

        # Botón tapas mejor valoradas
        self.btnMejorValoradas = QPushButton("Ver tapas mejor valoradas")
        layout.addWidget(self.btnMejorValoradas)
        self.btnMejorValoradas.clicked.connect(self.mostrar_mejor_valoradas)

        self.setLayout(layout)

        # DAOs
        self.tapaDAO = TapaDAO()
        self.pedidoDAO = PedidoDAO()
        self.cargar_tapas()

        self.btnHacerPedido.clicked.connect(self.hacer_pedido)

        #Botón cerrar sesión
        self.btnCerrarSesion = QPushButton("Cerrar sesión")
        self.btnCerrarSesion.clicked.connect(self.cerrar_sesion)
        layout.addWidget(self.btnCerrarSesion)

    def cerrar_sesion(self):
        self.close()
        from vistas.login_view import VentanaLogin
        self.login = VentanaLogin(self.coordinador)
        self.login.show()

    
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

        pedido = PedidoVO(self.usuario_id, id_tapa, cantidad, estado="En preparación")
        self.pedidoDAO.insertar_pedido(pedido)

        QMessageBox.information(self, "Pedido realizado", "Tu pedido ha sido enviado a la cocina.")

    def abrir_historial(self):
        self.ventana_historial = VentanaPedidosCliente(self.usuario_id)
        self.ventana_historial.show()

    def abrir_valoracion(self):
        self.ventana_valoracion = VentanaValoracion(self.usuario_id)
        self.ventana_valoracion.show()
        
    def mostrar_mas_vendidas(self):
        self.estadistica = VentanaEstadisticas("mas_vendidas", modo="usuario")
        self.estadistica.exec_()


    def mostrar_mejor_valoradas(self):
        self.estadistica = VentanaEstadisticas("mejor_valoradas")
        self.estadistica.exec_()