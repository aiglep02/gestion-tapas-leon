# vistas/login_view.py

from PyQt5.QtWidgets import QDialog, QDesktopWidget
from vistas.login import Ui_Dialog

class VentanaLogin(QDialog):
    def __init__(self, coordinador):  
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.coordinador = coordinador  

        # ✅ Establecer tamaño fijo de la ventana
        self.setFixedSize(500, 600)  # Ajusta si quieres más compacto

        # ✅ Centrar ventana en pantalla
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        # ✅ Conectar botones
        self.ui.btnLogin.clicked.connect(self.login)
        self.ui.botonRegistro.clicked.connect(self.abrir_registro)
        self.ui.botonAnonimo.clicked.connect(self.entrar_como_invitado)

    def login(self):
        email = self.ui.lineEdit.text()
        contrasena = self.ui.lineEdit_2.text()
        self.coordinador.login(email, contrasena, self)

    def mostrar_error(self, mensaje):
        self.ui.labelError.setText(mensaje)

    def abrir_registro(self):
        self.coordinador.mostrar_registro()

    def entrar_como_invitado(self):
        self.coordinador.mostrar_vista_invitado()
