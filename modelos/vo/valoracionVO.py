class ValoracionVO:
    def __init__(self, id_usuario, id_tapa, puntuacion, comentario):
        self.id_usuario = id_usuario
        self.id_tapa = id_tapa
        self.puntuacion = puntuacion
        self.comentario = comentario

    def __repr__(self):
        return (f"<ValoracionVO usuario={self.id_usuario}, tapa={self.id_tapa}, "
                f"puntuacion={self.puntuacion}, comentario='{self.comentario}'>")
