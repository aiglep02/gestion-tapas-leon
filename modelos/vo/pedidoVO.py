class PedidoVO:
    def __init__(self, id_usuario, id_tapa, cantidad, estado="pendiente"):
        self.id_usuario = id_usuario
        self.id_tapa = id_tapa
        self.cantidad = cantidad
        self.estado = estado
