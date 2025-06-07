from modelos.dao.tapaDAO import TapaDAO

dao = TapaDAO()
tapas = dao.obtener_todas_las_tapas()
print(tapas)
