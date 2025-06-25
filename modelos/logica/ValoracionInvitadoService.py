from modelos.dao.valoracionDAO import ValoracionDAO
from modelos.vo.valoracionVO import ValoracionVO

class ValoracionInvitadoService:
    def __init__(self):
        self.valoracion_dao = ValoracionDAO()  

    def enviar_valoracion(self, id_tapa, puntuacion, comentario):
        # Para invitados, no hay id_usuario, se puede poner None o 0
        valoracion = ValoracionVO(
            id_usuario=None,  # o 0 si tu BD no acepta NULL
            id_tapa=id_tapa,
            puntuacion=puntuacion,
            comentario=comentario
        )
        return self.valoracion_dao.insertar_valoracion(valoracion)
