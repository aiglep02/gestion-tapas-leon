from controladores.ControladorUsuarios import ControladorUsuarios
from modelos.ConexionMYSQL import ConexionMYSQL

conexion = ConexionMYSQL().conexion
usuarios = ControladorUsuarios(conexion)

# Ver usuarios
print("Usuarios registrados:")
for u in usuarios.obtener_usuarios():
    print(f"{u['id']} - {u['nombre']} ({u['email']}) - Rol: {u['rol']}")

# Eliminar usuario de prueba (opcional)
# usuarios.eliminar_usuario(3)

# Cambiar rol (por ejemplo a 'empleado')
#usuarios.actualizar_rol_usuario(6, 'empleado')

conexion.close()
