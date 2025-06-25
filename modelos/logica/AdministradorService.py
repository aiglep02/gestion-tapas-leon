from modelos.dao.tapaDAO import TapaDAO
from modelos.vo.tapaVO import TapaVO

class AdministradorService:
    def __init__(self):
        self.tapa_dao = TapaDAO()  

    def obtener_tapas(self):
        return self.tapa_dao.obtener_todas_las_tapas()

    def insertar_tapa(self, tapa: TapaVO):
        return self.tapa_dao.insertar_tapa(tapa)

    def actualizar_tapa(self, tapa_id, nombre=None, descripcion=None, stock=None):
        return self.tapa_dao.actualizar_tapa(tapa_id, nombre, descripcion, stock)

    def eliminar_tapa(self, tapa_id):
        return self.tapa_dao.eliminar_tapa(tapa_id)
