from modelos.ConexionMYSQL import conectar

class ControladorEstadisticas:
    def __init__(self):
        self.estrategia = None

    def set_estrategia(self, estrategia):
        self.estrategia = estrategia

    def calcular_estadisticas(self):
        if self.estrategia:
            conexion = conectar()  
            return self.estrategia.calcular(conexion)
        else:
            return []
