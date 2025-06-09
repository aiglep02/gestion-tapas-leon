from modelos.dao.valoracionDAO import ValoracionDAO
from modelos.vo.valoracionVO import ValoracionVO

class ValoracionInvitadoService:
    def __init__(self):
        self.valoracion_dao = ValoracionDAO()

    def enviar_valoracion(self, id_tapa, puntuacion, comentario):
        """
        Inserta una valoración para una tapa realizada por un invitado.
        Devuelve True si se inserta correctamente, False en caso contrario.
        """
        valoracion = ValoracionVO(
            id_usuario=None,  # Invitado no tiene ID de usuario
            id_tapa=id_tapa,
            puntuacion=puntuacion,
            comentario=comentario
        )
        return self.valoracion_dao.insertar_valoracion(valoracion)
