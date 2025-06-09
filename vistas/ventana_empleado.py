from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QHeaderView, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from controladores.ControladorEmpleado import ControladorEmpleado

class VentanaEmpleado(QWidget):
    def __init__(self, nombre_empleado, coordinador):
        super().__init__()
        self.setWindowTitle("Panel de Empleado")
        self.setMinimumSize(900, 400)
        self.nombre_empleado = nombre_empleado
        self.coordinador = coordinador
        self.controlador = ControladorEmpleado()

        with open("estilos/estilo.qss", "r") as f:
            self.setStyleSheet(f.read())

        layout = QVBoxLayout()

        # Botón cerrar sesión
        self.btnCerrarSesion = QPushButton("Cerrar sesión")
        self.btnCerrarSesion.setStyleSheet("background-color: red; color: white;")
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

        # Tabla de pedidos
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
        pedidos = self.controlador.obtener_pedidos_pendientes()
        self.tabla.setRowCount(len(pedidos))
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels(["ID Pedido", "ID Usuario", "ID Tapa", "Cantidad", "Estado", "Acciones"])

        for i, pedido in enumerate(pedidos):
            self.tabla.setItem(i, 0, QTableWidgetItem(str(pedido.id)))
            self.tabla.setItem(i, 1, QTableWidgetItem(str(pedido.id_usuario)))
            self.tabla.setItem(i, 2, QTableWidgetItem(str(pedido.id_tapa)))
            self.tabla.setItem(i, 3, QTableWidgetItem(str(pedido.cantidad)))
            self.tabla.setItem(i, 4, QTableWidgetItem(str(pedido.estado)))

            acciones_widget = QWidget()
            acciones_layout = QHBoxLayout()

            btn_preparar = QPushButton("Preparar")
            btn_preparar.clicked.connect(lambda _, pid=pedido.id: self.actualizar_estado(pid, "en preparación"))

            btn_listo = QPushButton("Listo")
            btn_listo.clicked.connect(lambda _, pid=pedido.id: self.actualizar_estado(pid, "listo"))

            btn_entregado = QPushButton("Entregado")
            # Cambio: ahora paso id_tapa correctamente para reducir stock por id
            btn_entregado.clicked.connect(lambda _, pid=pedido.id, id_tapa=pedido.id_tapa, cant=pedido.cantidad: self.entregar_pedido(pid, id_tapa, cant))

            for btn in (btn_preparar, btn_listo, btn_entregado):
                btn.setMinimumWidth(60)
                acciones_layout.addWidget(btn)

            acciones_layout.setSpacing(6)
            acciones_layout.setContentsMargins(0, 0, 0, 0)
            acciones_widget.setLayout(acciones_layout)
            self.tabla.setCellWidget(i, 5, acciones_widget)

    def actualizar_estado(self, id_pedido, nuevo_estado):
        exito = self.controlador.actualizar_estado_pedido(id_pedido, nuevo_estado)
        if exito:
            self.cargar_pedidos()

    def entregar_pedido(self, id_pedido, id_tapa, cantidad):
        exito = self.controlador.entregar_pedido(id_pedido, id_tapa, cantidad)
        if exito:
            self.cargar_pedidos()
