from estrategias.IEstrategiaEstadistica import IEstrategiaEstadistica

class EstadisticaTopValoradas(IEstrategiaEstadistica):
    def calcular(self, tapas):
        # Accedemos a la propiedad 'puntuacion_media' del objeto EstadisticaVO
        return sorted(tapas, key=lambda x: x.puntuacion_media, reverse=True)[:5]
