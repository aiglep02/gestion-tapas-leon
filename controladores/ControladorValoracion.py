from modelos.logica.ValoracionService import ValoracionService

class ControladorValoracion:
    def __init__(self, conexion): 
        self.service = ValoracionService(conexion)

    def obtener_tapas_entregadas(self, usuario_id):
        return self.service.obtener_tapas_entregadas(usuario_id)

    def enviar_valoracion(self, usuario_id, id_tapa, puntuacion, comentario):
        return self.service.insertar_valoracion(usuario_id, id_tapa, puntuacion, comentario)
