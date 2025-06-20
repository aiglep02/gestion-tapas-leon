from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QComboBox, QPushButton, QSpinBox, QMessageBox, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from controladores.ControladorClienteRegistrado import ControladorClienteRegistrado
from vistas.ventana_pedidos_cliente import VentanaPedidosCliente
from vistas.ventana_valoracion import VentanaValoracion
from vistas.ventana_estadisticas import VentanaEstadisticas

class VentanaClienteRegistrado(QWidget):
    def __init__(self, usuario_id, nombre, coordinador, conexion):
        super().__init__()
        self.setWindowTitle("Panel Cliente Registrado")
        self.setFixedSize(400, 420)
        self.usuario_id = usuario_id
        self.nombre = nombre
        self.coordinador = coordinador
        self.controlador = ControladorClienteRegistrado(conexion)

        with open("estilos/estilo.qss", "r") as f:
            self.setStyleSheet(f.read())

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

        # Bienvenida
        mensaje = QLabel(f"Bienvenido, {self.nombre}")
        mensaje.setAlignment(Qt.AlignCenter)
        mensaje.setFont(QFont("Arial", 16))
        layout.addWidget(mensaje)

        # UI de tapas
        self.comboTapas = QComboBox()
        layout.addWidget(self.comboTapas)

        self.spinCantidad = QSpinBox()
        self.spinCantidad.setMinimum(1)
        self.spinCantidad.setMaximum(10)
        layout.addWidget(self.spinCantidad)

        self.btnHacerPedido = QPushButton("Hacer pedido")
        self.btnHacerPedido.clicked.connect(self.hacer_pedido)
        layout.addWidget(self.btnHacerPedido)

        self.btnVerPedidos = QPushButton("Ver mis pedidos")
        self.btnVerPedidos.clicked.connect(self.abrir_historial)
        layout.addWidget(self.btnVerPedidos)

        self.btnValorar = QPushButton("Valorar tapas")
        self.btnValorar.clicked.connect(self.abrir_valoracion)
        layout.addWidget(self.btnValorar)

        self.btnMasVendidas = QPushButton("Ver tapas más vendidas")
        self.btnMasVendidas.clicked.connect(self.mostrar_mas_vendidas)
        layout.addWidget(self.btnMasVendidas)

        self.btnMejorValoradas = QPushButton("Ver tapas mejor valoradas")
        self.btnMejorValoradas.clicked.connect(self.mostrar_mejor_valoradas)
        layout.addWidget(self.btnMejorValoradas)

        self.btnCerrarSesion = QPushButton("Cerrar sesión")
        self.btnCerrarSesion.setStyleSheet("background-color: red; color: white;")
        self.btnCerrarSesion.clicked.connect(self.cerrar_sesion)
        layout.addWidget(self.btnCerrarSesion)

        self.setLayout(layout)
        self.cargar_tapas()

    def cerrar_sesion(self):
        self.close()
        from vistas.login_view import VentanaLogin
        self.login = VentanaLogin(self.coordinador)
        self.login.show()

    def mostrar_ayuda(self):
        QMessageBox.information(
            self,
            "Ayuda - Panel Cliente",
            "Desde aquí puedes:\n"
            "- Ver tapas disponibles y realizar pedidos\n"
            "- Consultar tu historial de pedidos\n"
            "- Valorar tapas que hayas probado\n"
            "- Ver las tapas más pedidas y mejor valoradas\n"
            "- Cerrar sesión para volver al login"
        )

    def cargar_tapas(self):
        tapas = self.controlador.obtener_tapas_disponibles()
        self.comboTapas.clear()
        self.comboTapas.addItem("Selecciona una tapa", None)

        for tapa in tapas:
            if tapa.stock == 0:
                texto = f"{tapa.nombre} (No disponible)"
                self.comboTapas.addItem(texto, None)
            else:
                texto = f"{tapa.nombre} (Stock: {tapa.stock})"
                self.comboTapas.addItem(texto, tapa.id_tapa)

    def hacer_pedido(self):
        id_tapa = self.comboTapas.currentData()
        cantidad = self.spinCantidad.value()

        if not id_tapa:
            QMessageBox.warning(self, "Error", "Debes seleccionar una tapa.")
            return

        exito, mensaje = self.controlador.hacer_pedido(self.usuario_id, id_tapa, cantidad)
        if exito:
            QMessageBox.information(self, "Pedido realizado", mensaje)
        else:
            QMessageBox.warning(self, "Error", mensaje)

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
