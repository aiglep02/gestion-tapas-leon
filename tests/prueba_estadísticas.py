from controladores.ControladorEstadisticas import ControladorEstadisticas
from modelos.ConexionMYSQL import ConexionMYSQL

conexion = ConexionMYSQL().conexion
estad = ControladorEstadisticas(conexion)

print("Tapas más pedidas:")
for t in estad.tapas_mas_pedidas():
    print(f"{t['nombre']}: {t['total_pedida']} unidades")

print("\nPedidos por estado:")
for p in estad.pedidos_por_estado():
    print(f"{p['estado']}: {p['cantidad']} pedidos")

conexion.close()
