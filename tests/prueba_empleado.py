from controladores.ControladorEmpleado import ControladorEmpleado
from modelos.ConexionMYSQL import ConexionMYSQL

conexion = ConexionMYSQL().conexion
empleado = ControladorEmpleado(conexion)

# Obtener pedidos pendientes
print("Pedidos pendientes:")
for pedido in empleado.obtener_pedidos_pendientes():
    print(f"Pedido {pedido['id']} de {pedido['cliente']} - Estado: {pedido['estado']}")

# Ver líneas de un pedido específico (ajusta ID si lo necesitas)
pedido_id = int(input("ID del pedido para ver detalles: "))
lineas = empleado.obtener_lineas_pedido(pedido_id)
print(f"Detalles del pedido {pedido_id}:")
for linea in lineas:
    print(f" - {linea['nombre']} x{linea['cantidad']}")

# Cambiar estado del pedido (por ejemplo, a "listo")
nuevo_estado = input("Nuevo estado (pendiente / en preparación / listo / entregado): ")
actualizados = empleado.actualizar_estado_pedido(pedido_id, nuevo_estado)
if actualizados:
    print(f"Pedido {pedido_id} actualizado a '{nuevo_estado}'")
else:
    print("No se pudo actualizar el estado.")

conexion.close()
