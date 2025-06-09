class EstadisticaVO:
    def __init__(self, nombre, total_pedida=0, puntuacion_media=0):
        self.nombre = nombre
        self.total_pedida = total_pedida
        self.puntuacion_media = puntuacion_media

    def __repr__(self):
        return (f"<EstadisticaVO nombre={self.nombre}, "
                f"total_pedida={self.total_pedida}, puntuacion_media={self.puntuacion_media}>")
