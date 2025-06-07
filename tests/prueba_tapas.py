from controladores.ControladorTapa import ControladorTapa
from modelos.ConexionMYSQL import ConexionMYSQL

conexion = ConexionMYSQL().conexion
tapa_ctrl = ControladorTapa(conexion)

# Listar tapas existentes
print("📋 Lista de tapas:")
for tapa in tapa_ctrl.obtener_tapas():
    print(f"{tapa['id']}: {tapa['nombre']} ({tapa['precio']}€) - Stock: {tapa['stock']}")

# Añadir una tapa nueva (si quieres probar)
#tapa_id = tapa_ctrl.insertar_tapa("Morcilla", "Clásica de León", 2.20, 10)
#print(f"✅ Tapa insertada con ID: {tapa_id}")

conexion.close()
