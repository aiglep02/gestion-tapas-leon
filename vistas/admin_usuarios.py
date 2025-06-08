from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QPushButton, QHBoxLayout, QMessageBox
from vistas.ventana_admin_usuarios import Ui_AdminUsuarios 
from modelos.ConexionMYSQL import conectar

class AdminUsuarios(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_AdminUsuarios()
        self.ui.setupUi(self)
        self.setWindowTitle("Gestión de Usuarios")

        # Aplicar estilos
        with open("estilos/estilo.qss", "r") as f:
            self.setStyleSheet(f.read())

        # Conexión a base de datos
        self.db = conectar()

        # Añadir botón de ayuda "?" en tiempo de ejecución
        self.boton_ayuda = QPushButton("?")
        self.boton_ayuda.setFixedSize(30, 30)
        self.boton_ayuda.setToolTip("Ayuda sobre esta pantalla")
        self.boton_ayuda.clicked.connect(self.mostrar_ayuda)

        ayuda_layout = QHBoxLayout()
        ayuda_layout.setContentsMargins(0, 0, 0, 0)
        ayuda_layout.addWidget(self.boton_ayuda)
        self.ui.verticalLayout.insertLayout(0, ayuda_layout)

        # Cargar tabla al iniciar
        self.cargar_usuarios()

        # Eventos
        self.ui.Eliminar.clicked.connect(self.eliminar_usuario)
        self.ui.Actualizar.clicked.connect(self.cargar_usuarios)
        self.ui.CambiarRol.clicked.connect(self.cambiar_rol)

    def cargar_usuarios(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT id, nombre, email, rol FROM usuario")
        usuarios = cursor.fetchall()

        self.ui.tablaUsuarios.setRowCount(len(usuarios))
        for i, (id_, nombre, email, rol) in enumerate(usuarios):
            self.ui.tablaUsuarios.setItem(i, 0, QTableWidgetItem(str(id_)))
            self.ui.tablaUsuarios.setItem(i, 1, QTableWidgetItem(nombre))
            self.ui.tablaUsuarios.setItem(i, 2, QTableWidgetItem(email))
            self.ui.tablaUsuarios.setItem(i, 3, QTableWidgetItem(rol))

    def eliminar_usuario(self):
        fila = self.ui.tablaUsuarios.currentRow()
        if fila >= 0:
            id_usuario = self.ui.tablaUsuarios.item(fila, 0).text()
            cursor = self.db.cursor()
            cursor.execute("DELETE FROM usuario WHERE id = %s", (id_usuario,))
            self.db.commit()
            self.cargar_usuarios()

    def cambiar_rol(self):
        fila = self.ui.tablaUsuarios.currentRow()
        nuevo_rol = self.ui.Rol.currentText()
        if fila >= 0:
            id_usuario = self.ui.tablaUsuarios.item(fila, 0).text()
            cursor = self.db.cursor()
            cursor.execute("UPDATE usuario SET rol = %s WHERE id = %s", (nuevo_rol, id_usuario))
            self.db.commit()
            self.cargar_usuarios()

    def mostrar_ayuda(self):
        QMessageBox.information(
            self,
            "Ayuda - Gestión de Usuarios",
            "Desde esta pantalla puedes:\n"
            "- Consultar todos los usuarios registrados en el sistema.\n"
            "- Cambiar el rol de un usuario (cliente, empleado, administrador).\n"
            "- Eliminar usuarios de la base de datos.\n\n"
            "Cuidado: No hay confirmación al eliminar un usuario."
        )
