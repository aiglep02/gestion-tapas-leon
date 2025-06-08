class PedidoVO:
    def __init__(self, id_usuario, id_tapa=None, cantidad=None, id=None, estado="En preparación"):
        self.id = id
        self.id_usuario = id_usuario
        self.id_tapa = id_tapa
        self.cantidad = cantidad
        self.estado = estado