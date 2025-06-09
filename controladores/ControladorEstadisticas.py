from modelos.ConexionMYSQL import conectar
from modelos.dao.pedidoDAO import PedidoDAO

class ControladorEstadisticas:
    def __init__(self):
        self.estrategia = None

    def set_estrategia(self, estrategia):
        self.estrategia = estrategia

    def calcular_estadisticas(self):
        if self.estrategia:
            dao = PedidoDAO()
            datos = dao.obtener_datos_para_estadisticas()
            return self.estrategia.calcular(datos)
        else:
            return []