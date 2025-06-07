class TapaVO:
    def __init__(self, id_tapa=None, nombre="", descripcion="", precio=0.0, stock=0, imagen=None):
        self.id_tapa = id_tapa
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock
        self.imagen = imagen
