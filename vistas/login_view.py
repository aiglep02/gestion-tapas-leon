# vistas/login_view.py

from PyQt5.QtWidgets import QDialog
from vistas.login import Ui_Dialog

class VentanaLogin(QDialog):
    def __init__(self, coordinador):  
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.coordinador = coordinador  

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
