from estrategias.IEstrategiaEstadistica import IEstrategiaEstadistica

class EstadisticaTopValoradas(IEstrategiaEstadistica):
    def calcular(self, tapas):
        return sorted(tapas, key=lambda x: x["puntuacion_media"], reverse=True)[:5]
