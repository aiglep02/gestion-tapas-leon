from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QComboBox, QPushButton, QSpinBox,
    QTextEdit, QMessageBox, QHBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from modelos.logica.invitadoService import InvitadoService
from vistas.ventana_estadisticas import VentanaEstadisticas
from vistas.ventana_valoracion_invitado import VentanaValoracionInvitado

class VentanaInvitado(QWidget):
    def __init__(self, coordinador):
        super().__init__()
        self.setWindowTitle("Explorar como Invitado")
        self.setFixedSize(400, 430)
        self.coordinador = coordinador

        # El service gestiona internamente la conexión
        self.service = InvitadoService()

        with open("estilos/estilo.qss", "r") as f:
            self.setStyleSheet(f.read())

        layout = QVBoxLayout()

        # Ayuda
        ayuda_layout = QHBoxLayout()
        ayuda_layout.setAlignment(Qt.AlignRight)
        boton_ayuda = QPushButton("?")
        boton_ayuda.setFixedSize(30, 30)
        boton_ayuda.setToolTip("Ayuda sobre esta pantalla")
        boton_ayuda.clicked.connect(self.mostrar_ayuda)
        ayuda_layout.addWidget(boton_ayuda)
        layout.addLayout(ayuda_layout)

        # Bienvenida
        mensaje = QLabel("Bienvenido, invitado")
        mensaje.setAlignment(Qt.AlignCenter)
        mensaje.setFont(QFont("Arial", 16))
        layout.addWidget(mensaje)

        # Selector de tapas
        self.comboTapas = QComboBox()
        layout.addWidget(self.comboTapas)

        # Cantidad
        self.spinCantidad = QSpinBox()
        self.spinCantidad.setMinimum(1)
        self.spinCantidad.setMaximum(10)
        layout.addWidget(self.spinCantidad)

        # Botones de acción
        self.btnHacerPedido = QPushButton("Hacer pedido")
        self.btnHacerPedido.clicked.connect(self.hacer_pedido)
        layout.addWidget(self.btnHacerPedido)

        self.btnMasVendidas = QPushButton("Ver tapas más vendidas")
        self.btnMasVendidas.clicked.connect(self.mostrar_mas_vendidas)
        layout.addWidget(self.btnMasVendidas)

        self.btnMejorValoradas = QPushButton("Ver tapas mejor valoradas")
        self.btnMejorValoradas.clicked.connect(self.mostrar_mejor_valoradas)
        layout.addWidget(self.btnMejorValoradas)

        self.btnValorar = QPushButton("Valorar una tapa")
        self.btnValorar.clicked.connect(self.abrir_valoracion)
        layout.addWidget(self.btnValorar)

        self.btnCerrarSesion = QPushButton("Cerrar sesión")
        self.btnCerrarSesion.setStyleSheet("background-color: red; color: white;")
        self.btnCerrarSesion.clicked.connect(self.cerrar_sesion)
        layout.addWidget(self.btnCerrarSesion)

        self.setLayout(layout)

        self.cargar_tapas()

        if not hasattr(VentanaValoracionInvitado, "tapas_pedidas"):
            VentanaValoracionInvitado.tapas_pedidas = []

    def mostrar_ayuda(self):
        QMessageBox.information(
            self,
            "Ayuda - Invitado",
            "Como invitado puedes:\n"
            "- Ver tapas disponibles\n"
            "- Realizar un pedido sin registrarte\n"
            "- Consultar tapas más pedidas y mejor valoradas\n"
            "- Valorar tapas que has pedido\n\n"
            "Para guardar historial, regístrate como cliente."
        )

    def cargar_tapas(self):
        tapas = self.service.obtener_tapas_disponibles()
        self.comboTapas.clear()
        self.comboTapas.addItem("Selecciona una tapa", None)
        for tapa in tapas:
            texto = f"{tapa.nombre} (No disponible)" if tapa.stock == 0 else f"{tapa.nombre} (Stock: {tapa.stock})"
            self.comboTapas.addItem(texto, tapa.id_tapa if tapa.stock > 0 else None)

    def hacer_pedido(self):
        id_tapa = self.comboTapas.currentData()
        cantidad = self.spinCantidad.value()
        if not id_tapa:
            QMessageBox.warning(self, "Error", "Debes seleccionar una tapa.")
            return

        exito, mensaje = self.service.hacer_pedido_invitado(id_tapa, cantidad)
        if exito:
            nombre_tapa = self.comboTapas.currentText().split(" (")[0]
            VentanaValoracionInvitado.tapas_pedidas.append((id_tapa, nombre_tapa))
            QMessageBox.information(self, "Pedido realizado", mensaje)
        else:
            QMessageBox.critical(self, "Error", mensaje)

    def mostrar_mas_vendidas(self):
        # Llamada corregida: sólo tipo y modo
        self.estadistica = VentanaEstadisticas("mas_vendidas", modo="usuario")
        self.estadistica.exec_()

    def mostrar_mejor_valoradas(self):
        # Llamada corregida: sólo tipo
        self.estadistica = VentanaEstadisticas("mejor_valoradas")
        self.estadistica.exec_()

    def abrir_valoracion(self):
        self.ventana_valoracion = VentanaValoracionInvitado(VentanaValoracionInvitado.tapas_pedidas)
        self.ventana_valoracion.show()

    def cerrar_sesion(self):
        self.close()
        from vistas.login_view import VentanaLogin
        self.login = VentanaLogin(self.coordinador)
        self.login.show()
