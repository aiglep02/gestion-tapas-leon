from modelos.dao.tapaDAO import TapaDAO
from modelos.vo.EstadisticaVO import EstadisticaVO

class EstadisticaService:
    def __init__(self):
        self.tapa_dao = TapaDAO()

    def obtener_estadisticas(self):
        estadisticas_crudas = self.tapa_dao.obtener_datos_para_estadisticas()
        estadisticas = []

        for fila in estadisticas_crudas:
            estadistica = EstadisticaVO(
                nombre=fila.nombre,
                total_pedida=fila.total_pedida,
                puntuacion_media=fila.puntuacion_media
            )
            estadisticas.append(estadistica)

        return estadisticas
