class ContextoEstadisticas:
    def __init__(self, estrategia):
        self.estrategia = estrategia

    def ejecutar(self, datos):
        return self.estrategia.calcular(datos)

    def cambiar_estrategia(self, nueva_estrategia):
        self.estrategia = nueva_estrategia