from modelos.logica.ValoracionInvitadoService import ValoracionInvitadoService

class ControladorValoracionInvitado:
    def __init__(self):
        self.service = ValoracionInvitadoService()  
        
    def enviar_valoracion(self, id_tapa, puntuacion, comentario):
        """
        Envía la valoración usando el service.
        Devuelve True si se guardó correctamente, False en caso contrario.
        """
        return self.service.enviar_valoracion(id_tapa, puntuacion, comentario)
