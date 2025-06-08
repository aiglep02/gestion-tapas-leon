# main.py
import sys
from PyQt5.QtWidgets import QApplication
from controladores.Coordinador import Coordinador
from modelos.ConexionMYSQL import conectar
from vistas.login_view import VentanaLogin

if __name__ == "__main__":
    app = QApplication(sys.argv)

    conexion = conectar()
    coordinador = Coordinador(conexion)
    login = VentanaLogin(coordinador)  # ← ya no da error
    login.show()

    sys.exit(app.exec_())