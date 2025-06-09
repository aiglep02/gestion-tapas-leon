from modelos.logica.EstadisticaService import EstadisticaService

class ControladorEstadisticas:
    def __init__(self):
        self.service = EstadisticaService()
        self.estrategia = None

    def set_estrategia(self, estrategia):
        """
        Define la estrategia para calcular estadísticas.
        La estrategia debe implementar un método `calcular(datos)`.
        """
        self.estrategia = estrategia

    def calcular_estadisticas(self):
        """
        Obtiene datos sin procesar del servicio y los procesa con la estrategia definida.
        Devuelve la lista procesada de estadísticas.
        """
        datos = self.service.obtener_estadisticas()
        if self.estrategia:
            return self.estrategia.calcular(datos)
        return datos
