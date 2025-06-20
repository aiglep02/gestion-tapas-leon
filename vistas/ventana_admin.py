from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QMessageBox,
    QHBoxLayout, QTableWidget, QTableWidgetItem, QInputDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from estrategias.EstadisticaTopTapas import EstadisticaTopTapas
from estrategias.EstadisticaTopValoradas import EstadisticaTopValoradas
from controladores.ControladorEstadisticas import ControladorEstadisticas
from controladores.ControladorAdministrador import ControladorAdministrador
from modelos.ConexionJDBC import conectar
from vistas.admin_usuarios import AdminUsuarios

class VentanaAdmin(QWidget):
    def __init__(self, nombre_admin, coordinador):
        super().__init__()
        self.nombre_admin = nombre_admin
        self.setWindowTitle("Panel Administrador")
        self.setMinimumSize(600, 500)
        self.coordinador = coordinador

        with open("estilos/estilo.qss", "r") as f:
            self.setStyleSheet(f.read())

        self.conexion = conectar()
        self.controlador = ControladorAdministrador(self.conexion)

        layout = QVBoxLayout()

        self.btnCerrarSesion = QPushButton("Cerrar sesión")
        self.btnCerrarSesion.setStyleSheet("background-color: red; color: white;")
        self.btnCerrarSesion.clicked.connect(self.cerrar_sesion)
        layout.addWidget(self.btnCerrarSesion)

        ayuda_layout = QHBoxLayout()
        ayuda_layout.setAlignment(Qt.AlignRight)
        boton_ayuda = QPushButton("?")
        boton_ayuda.setFixedSize(30, 30)
        boton_ayuda.setToolTip("Ayuda sobre esta pantalla")
        boton_ayuda.clicked.connect(self.mostrar_ayuda)
        ayuda_layout.addWidget(boton_ayuda)
        layout.addLayout(ayuda_layout)

        mensaje = QLabel(f"Bienvenido, {self.nombre_admin}")
        mensaje.setAlignment(Qt.AlignCenter)
        mensaje.setFont(QFont("Arial", 16))
        layout.addWidget(mensaje)

        self.btnVerTapas = QPushButton("Ver todas las tapas")
        self.btnVerTapas.clicked.connect(self.mostrar_tapas)
        layout.addWidget(self.btnVerTapas)

        self.btnAnadirTapa = QPushButton("Añadir nueva tapa")
        self.btnAnadirTapa.clicked.connect(self.anadir_tapa)
        layout.addWidget(self.btnAnadirTapa)

        self.btnEditarTapa = QPushButton("Editar tapa seleccionada")
        self.btnEditarTapa.clicked.connect(self.editar_tapa)
        layout.addWidget(self.btnEditarTapa)

        self.btnEliminarTapa = QPushButton("Eliminar tapa seleccionada")
        self.btnEliminarTapa.clicked.connect(self.eliminar_tapa)
        layout.addWidget(self.btnEliminarTapa)

        self.btnEstadisticas = QPushButton("Ver tapas más pedidas")
        self.btnEstadisticas.clicked.connect(self.mostrar_estadisticas)
        layout.addWidget(self.btnEstadisticas)

        self.btnVerValoradas = QPushButton("Ver tapas mejor valoradas")
        self.btnVerValoradas.clicked.connect(self.mostrar_valoradas)
        layout.addWidget(self.btnVerValoradas)

        self.btnGestionUsuarios = QPushButton("Gestionar usuarios")
        self.btnGestionUsuarios.clicked.connect(self.abrir_gestion_usuarios)
        layout.addWidget(self.btnGestionUsuarios)

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
            "En este panel puedes:\n"
            "- Consultar tapas\n- Añadir nuevas tapas\n- Editar o eliminar tapas\n"
            "- Consultar estadísticas\n- Gestionar usuarios\n- Cerrar sesión"
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

    def mostrar_tapas(self):
        tapas = self.controlador.obtener_tapas()
        self.tabla.setRowCount(len(tapas))
        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre", "Descripción", "Stock"])

        for i, tapa in enumerate(tapas):
            self.tabla.setItem(i, 0, QTableWidgetItem(str(tapa.id_tapa)))
            self.tabla.setItem(i, 1, QTableWidgetItem(tapa.nombre))
            self.tabla.setItem(i, 2, QTableWidgetItem(tapa.descripcion or ""))
            self.tabla.setItem(i, 3, QTableWidgetItem(str(tapa.stock)))

    def anadir_tapa(self):
        nombre, ok1 = QInputDialog.getText(self, "Añadir tapa", "Nombre:")
        if not ok1 or not nombre:
            return
        descripcion, ok2 = QInputDialog.getText(self, "Añadir tapa", "Descripción:")
        if not ok2:
            return
        stock, ok3 = QInputDialog.getInt(self, "Añadir tapa", "Stock inicial:", 0)
        if not ok3:
            return
        self.controlador.insertar_tapa(nombre, descripcion, precio=0, stock=stock)
        self.mostrar_tapas()

    def editar_tapa(self):
        fila = self.tabla.currentRow()
        if fila < 0:
            QMessageBox.warning(self, "Editar", "Selecciona una tapa.")
            return
        tapa_id = int(self.tabla.item(fila, 0).text())
        nuevo_stock, ok = QInputDialog.getInt(self, "Editar tapa", "Nuevo stock:", 0)
        if ok:
            self.controlador.actualizar_tapa(tapa_id, stock=nuevo_stock)
            self.mostrar_tapas()

    def eliminar_tapa(self):
        fila = self.tabla.currentRow()
        if fila < 0:
            QMessageBox.warning(self, "Eliminar", "Selecciona una tapa.")
            return
        tapa_id = int(self.tabla.item(fila, 0).text())
        confirmacion = QMessageBox.question(
            self,
            "Confirmar eliminación",
            f"¿Seguro que quieres eliminar la tapa ID {tapa_id}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirmacion == QMessageBox.Yes:
            self.controlador.eliminar_tapa(tapa_id)
            self.mostrar_tapas()

    def abrir_gestion_usuarios(self):
        self.ventana_usuarios = AdminUsuarios()
        self.ventana_usuarios.show()
