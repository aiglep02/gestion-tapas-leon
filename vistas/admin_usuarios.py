from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QPushButton, QHBoxLayout, QMessageBox
from vistas.ui_admin_usuarios import Ui_AdminUsuarios
from controladores.ControladorAdminUsuarios import ControladorAdminUsuarios
from vistas.ventana_crear_usuario import VentanaCrearUsuario

class AdminUsuarios(QDialog):
    def __init__(self, conexion):
        super().__init__()
        self.ui = Ui_AdminUsuarios()
        self.ui.setupUi(self)
        self.setWindowTitle("Gestión de Usuarios")
        self.conexion = conexion

        # Aplicar estilos
        with open("estilos/estilo.qss", "r") as f:
            self.setStyleSheet(f.read())

        # ✅ Conexión inyectada al controlador
        self.controlador = ControladorAdminUsuarios(conexion)

        # Botón de ayuda
        boton_ayuda = QPushButton("?")
        boton_ayuda.setFixedSize(30, 30)
        boton_ayuda.setToolTip("Ayuda sobre esta pantalla")
        boton_ayuda.clicked.connect(self.mostrar_ayuda)

        # Añadir al layout principal si existe
        if hasattr(self.ui, "verticalLayout"):
            ayuda_layout = QHBoxLayout()
            ayuda_layout.setContentsMargins(0, 0, 0, 0)
            ayuda_layout.addWidget(boton_ayuda)
            self.ui.verticalLayout.insertLayout(0, ayuda_layout)

        # Conectar eventos
        self.ui.Eliminar.clicked.connect(self.eliminar_usuario)
        self.ui.btnActualizar.clicked.connect(self.cambiar_rol)
        self.ui.btnAbrirCrearUsuario.clicked.connect(self.abrir_crear_usuario)
        self.ui.Rol.setCurrentIndex(0)

        # Cargar usuarios al iniciar
        self.cargar_usuarios()

    def cargar_usuarios(self):
        usuarios = self.controlador.listar_usuarios()
        self.ui.tablaUsuarios.setRowCount(len(usuarios))
        for i, usuario in enumerate(usuarios):
            self.ui.tablaUsuarios.setItem(i, 0, QTableWidgetItem(str(usuario.id_usuario)))
            self.ui.tablaUsuarios.setItem(i, 1, QTableWidgetItem(usuario.nombre))
            self.ui.tablaUsuarios.setItem(i, 2, QTableWidgetItem(usuario.email))
            self.ui.tablaUsuarios.setItem(i, 3, QTableWidgetItem(usuario.rol))

    def eliminar_usuario(self):
        fila = self.ui.tablaUsuarios.currentRow()
        if fila >= 0:
            id_usuario = int(self.ui.tablaUsuarios.item(fila, 0).text())

            confirm = QMessageBox.question(
                self,
                "Confirmar eliminación",
                "¿Estás seguro de que deseas eliminar este usuario?",
                QMessageBox.Yes | QMessageBox.No
            )

            if confirm == QMessageBox.Yes:
                try:
                    self.controlador.eliminar_usuario(id_usuario)
                    QMessageBox.information(self, "Éxito", "Usuario eliminado correctamente.")
                    self.cargar_usuarios()
                except Exception as e:
                    QMessageBox.warning(self, "No se puede eliminar", str(e))

    def abrir_crear_usuario(self):
        # ✅ Pasa también la conexión a la ventana de crear usuario
        self.ventana_crear_usuario = VentanaCrearUsuario(self.conexion)
        resultado = self.ventana_crear_usuario.exec_()
        if resultado == 1:
            self.cargar_usuarios()

    def cambiar_rol(self):
        fila = self.ui.tablaUsuarios.currentRow()
        nuevo_rol = self.ui.Rol.currentText()
        if fila >= 0:
            id_usuario = int(self.ui.tablaUsuarios.item(fila, 0).text())
            self.controlador.cambiar_rol(id_usuario, nuevo_rol)
            self.cargar_usuarios()

    def mostrar_ayuda(self):
        QMessageBox.information(
            self,
            "Ayuda - Gestión de Usuarios",
            "Desde esta pantalla puedes:\n"
            "- Consultar todos los usuarios registrados.\n"
            "- Cambiar el rol de un usuario.\n"
            "- Eliminar usuarios.\n\n"
            "⚠️ No hay confirmación al eliminar."
        )
