from PyQt5.QtWidgets import QDialog, QMessageBox, QTableWidgetItem
from vistas.admin_usuarios import Ui_AdminUsuarios
from controladores.ControladorUsuarios import ControladorUsuarios
from modelos.ConexionMYSQL import ConexionMYSQL
import os

class VentanaAdminUsuarios(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_AdminUsuarios()
        self.ui.setupUi(self)

        # Aplicar estilo visual si existe
        ruta_estilo = os.path.join("estilos", "estilo.qss")
        if os.path.exists(ruta_estilo):
            with open(ruta_estilo, "r") as f:
                self.setStyleSheet(f.read())

        # Conexión a base de datos y controlador
        self.conexion = ConexionMYSQL().conexion
        self.controlador = ControladorUsuarios(self.conexion)

        # Conectar señales de botones
        self.ui.Actualizar.clicked.connect(self.cargar_usuarios)
        self.ui.Eliminar.clicked.connect(self.eliminar_usuario)
        self.ui.CambiarRol.clicked.connect(self.cambiar_rol)

        # Cargar usuarios al iniciar
        self.cargar_usuarios()

    def cargar_usuarios(self):
        self.ui.tablaUsuarios.setRowCount(0)
        usuarios = self.controlador.obtener_usuarios()

        for row_idx, usuario in enumerate(usuarios):
            self.ui.tablaUsuarios.insertRow(row_idx)
            self.ui.tablaUsuarios.setItem(row_idx, 0, QTableWidgetItem(str(usuario["id"])))
            self.ui.tablaUsuarios.setItem(row_idx, 1, QTableWidgetItem(usuario["nombre"]))
            self.ui.tablaUsuarios.setItem(row_idx, 2, QTableWidgetItem(usuario["email"]))
            self.ui.tablaUsuarios.setItem(row_idx, 3, QTableWidgetItem(usuario["rol"]))

    def obtener_usuario_seleccionado(self):
        fila = self.ui.tablaUsuarios.currentRow()
        if fila < 0:
            return None
        return int(self.ui.tablaUsuarios.item(fila, 0).text())

    def eliminar_usuario(self):
        usuario_id = self.obtener_usuario_seleccionado()
        if usuario_id:
            confirm = QMessageBox.question(self, "Confirmar", "¿Eliminar este usuario?", QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                self.controlador.eliminar_usuario(usuario_id)
                self.cargar_usuarios()

    def cambiar_rol(self):
        usuario_id = self.obtener_usuario_seleccionado()
        nuevo_rol = self.ui.Rol.currentText()
        if usuario_id:
            self.controlador.actualizar_rol_usuario(usuario_id, nuevo_rol)
            self.cargar_usuarios()
