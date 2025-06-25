import sys
from PyQt5.QtWidgets import QApplication
from controladores.Coordinador import Coordinador
from vistas.login_view import VentanaLogin

if __name__ == "__main__":
    app = QApplication(sys.argv)

    coordinador = Coordinador()  
    login = VentanaLogin(coordinador)
    login.show()

    sys.exit(app.exec_())
