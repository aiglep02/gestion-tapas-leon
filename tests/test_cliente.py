from vistas.ventana_cliente import VentanaClienteRegistrado
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaClienteRegistrado(usuario_id=17)
    ventana.show()
    sys.exit(app.exec_())
