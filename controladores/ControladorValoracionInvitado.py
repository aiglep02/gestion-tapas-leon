from modelos.logica.ValoracionInvitadoService import ValoracionInvitadoService
from modelos.ConexionJDBC import conectar

class ControladorValoracionInvitado:
    def __init__(self):
        self.service = ValoracionInvitadoService(conectar())

    def enviar_valoracion(self, id_tapa, puntuacion, comentario):
        """
        Envía la valoración usando el service.
        Devuelve True si se guardó correctamente, False en caso contrario.
        """
        return self.service.enviar_valoracion(id_tapa, puntuacion, comentario)
