class TapaVO:
    def __init__(self, id_tapa=None, nombre=None, descripcion=None, stock=None):
        self.id_tapa = id_tapa
        self.nombre = nombre
        self.descripcion = descripcion
        self.stock = stock

    def __repr__(self):
        return (
            f"<TapaVO id_tapa={self.id_tapa}, nombre={self.nombre}, "
            f"descripcion={self.descripcion}, stock={self.stock}>"
        )
