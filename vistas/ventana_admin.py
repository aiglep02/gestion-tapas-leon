from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QMessageBox,
    QHBoxLayout, QTableWidget, QTableWidgetItem
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from estrategias.EstadisticaTopTapas import EstadisticaTopTapas
from estrategias.EstadisticaTopValoradas import EstadisticaTopValoradas
from controladores.ControladorEstadisticas import ControladorEstadisticas
from vistas.admin_usuarios import AdminUsuarios

class VentanaAdmin(QWidget):
    def __init__(self, nombre_admin, coordinador):
        super().__init__()
        self.nombre_admin = nombre_admin
        self.setWindowTitle("Panel Administrador")
        self.setMinimumSize(500, 400)
        self.coordinador = coordinador

        # Aplicar estilo
        with open("estilos/estilo.qss", "r") as f:
            self.setStyleSheet(f.read())

        layout = QVBoxLayout()

        self.btnCerrarSesion = QPushButton("Cerrar sesión")
        self.btnCerrarSesion.setStyleSheet("background-color: red; color: white;")
        self.btnCerrarSesion.clicked.connect(self.cerrar_sesion)
        layout.addWidget(self.btnCerrarSesion)

        # Botón de ayuda
        ayuda_layout = QHBoxLayout()
        ayuda_layout.setAlignment(Qt.AlignRight)
        boton_ayuda = QPushButton("?")
        boton_ayuda.setFixedSize(30, 30)
        boton_ayuda.setToolTip("Ayuda sobre esta pantalla")
        boton_ayuda.clicked.connect(self.mostrar_ayuda)
        ayuda_layout.addWidget(boton_ayuda)
        layout.addLayout(ayuda_layout)

        # Mensaje de bienvenida
        mensaje = QLabel(f"Bienvenido, {self.nombre_admin}")
        mensaje.setAlignment(Qt.AlignCenter)
        mensaje.setFont(QFont("Arial", 16))
        layout.addWidget(mensaje)

        # Botones de estadísticas
        self.btnEstadisticas = QPushButton("Ver tapas más pedidas")
        self.btnEstadisticas.clicked.connect(self.mostrar_estadisticas)
        layout.addWidget(self.btnEstadisticas)

        self.btnVerValoradas = QPushButton("Ver tapas mejor valoradas")
        self.btnVerValoradas.clicked.connect(self.mostrar_valoradas)
        layout.addWidget(self.btnVerValoradas)

        # Botón para gestionar usuarios
        self.btnGestionUsuarios = QPushButton("Gestionar usuarios")
        self.btnGestionUsuarios.setObjectName("btnGestionUsuarios")
        self.btnGestionUsuarios.clicked.connect(self.abrir_gestion_usuarios)
        layout.addWidget(self.btnGestionUsuarios)

        # Tabla para estadísticas
        self.tabla = QTableWidget()
        layout.addWidget(self.tabla)

        self.setLayout(layout)

    def cerrar_sesion(self):
        self.close()
        from vistas.login_view import VentanaLogin
        self.login = VentanaLogin(self.coordinador)
        self.login.show()

    def mostrar_ayuda(self):
        QMessageBox.information(
            self,
            "Ayuda - Panel Administrador",
            "En este panel puedes realizar las siguientes acciones:\n"
            "- Consultar las tapas más pedidas por los clientes\n"
            "- Ver las tapas mejor valoradas\n"
            "- Acceder a la gestión de usuarios registrados\n"
            "- Cerrar sesión para volver al login"
        )

    def mostrar_estadisticas(self):
        controlador = ControladorEstadisticas()
        controlador.set_estrategia(EstadisticaTopTapas())
        resultados = controlador.calcular_estadisticas()

        self.tabla.setRowCount(len(resultados))
        self.tabla.setColumnCount(2)
        self.tabla.setHorizontalHeaderLabels(["Tapa", "Total Pedidos"])

        for i, fila in enumerate(resultados):
            self.tabla.setItem(i, 0, QTableWidgetItem(fila.nombre))
            self.tabla.setItem(i, 1, QTableWidgetItem(str(fila.total_pedida)))

    def mostrar_valoradas(self):
        controlador = ControladorEstadisticas()
        controlador.set_estrategia(EstadisticaTopValoradas())
        resultados = controlador.calcular_estadisticas()

        self.tabla.setRowCount(len(resultados))
        self.tabla.setColumnCount(2)
        self.tabla.setHorizontalHeaderLabels(["Tapa", "Puntuación Media"])

        for i, fila in enumerate(resultados):
            self.tabla.setItem(i, 0, QTableWidgetItem(fila.nombre))
            self.tabla.setItem(i, 1, QTableWidgetItem(str(fila.puntuacion_media)))

    def abrir_gestion_usuarios(self):
        self.ventana_usuarios = AdminUsuarios()
        self.ventana_usuarios.show()
