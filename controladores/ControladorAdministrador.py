from modelos.logica.AdministradorService import AdministradorService
from modelos.vo.tapaVO import TapaVO

class ControladorAdministrador:
    def __init__(self, conexion):
        self.logica = AdministradorService(conexion)

    def obtener_tapas(self):
        return self.logica.obtener_tapas()

    def insertar_tapa(self, nombre, descripcion, stock):
        tapa = TapaVO(nombre=nombre, descripcion=descripcion, stock=stock)
        return self.logica.insertar_tapa(tapa)

    def actualizar_tapa(self, tapa_id, nombre=None, descripcion=None, stock=None):
        return self.logica.actualizar_tapa(tapa_id, nombre=nombre, descripcion=descripcion, stock=stock)

    def eliminar_tapa(self, tapa_id):
        return self.logica.eliminar_tapa(tapa_id)
