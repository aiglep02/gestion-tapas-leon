from controladores.ControladorAdministrador import ControladorAdministrador
from modelos.ConexionMYSQL import ConexionMYSQL

conexion = ConexionMYSQL().conexion
admin = ControladorAdministrador(conexion)

# Insertar una tapa
tapa_id = admin.insertar_tapa("Tapa admin", "Descripción admin", 3.00, 5)
print(f"Tapa insertada con ID: {tapa_id}")

# Actualizar la tapa
admin.actualizar_tapa(tapa_id, stock=10, precio=3.50)
print("Tapa actualizada.")

# Listar las tapas
for tapa in admin.obtener_tapas():
    print(f"{tapa['id']}: {tapa['nombre']} - {tapa['precio']}€ ({tapa['stock']} en stock)")

# Eliminar la tapa
admin.eliminar_tapa(tapa_id)
print("Tapa eliminada.")

conexion.close()
