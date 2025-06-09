from estrategias.IEstrategiaEstadistica import IEstrategiaEstadistica

class EstadisticaTopTapas(IEstrategiaEstadistica):
    def calcular(self, tapas):
        return sorted(tapas, key=lambda x: x["total_pedida"], reverse=True)