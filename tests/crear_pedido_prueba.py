from controladores.ControladorPedido import ControladorPedido
from modelos.ConexionMYSQL import ConexionMYSQL

conexion = ConexionMYSQL().conexion
cursor = conexion.cursor()

try:
    # 🔹 Crear tapas si no existen
    cursor.execute("SELECT COUNT(*) FROM tapa WHERE id IN (1, 2)")
    if cursor.fetchone()[0] < 2:
        cursor.execute("INSERT INTO tapa (id, nombre, descripcion, precio, stock) VALUES (1, 'Tortilla', 'Con cebolla', 2.50, 10)")
        cursor.execute("INSERT INTO tapa (id, nombre, descripcion, precio, stock) VALUES (2, 'Chorizo', 'Picante', 2.00, 8)")
        print("✅ Tapas de prueba insertadas.")

    # 🔹 Crear usuario si no existe
    cursor.execute("SELECT id FROM usuario WHERE email = 'empleado@tapas.com'")
    result = cursor.fetchone()
    if result:
        usuario_id = result[0]
    else:
        cursor.execute("INSERT INTO usuario (nombre, email, contraseña, rol) VALUES ('Empleado', 'empleado@tapas.com', '1234', 'cliente')")
        conexion.commit()
        cursor.execute("SELECT LAST_INSERT_ID()")
        usuario_id = cursor.fetchone()[0]
        print(f"✅ Usuario creado con ID: {usuario_id}")

    # 🔹 Crear pedido
    controlador = ControladorPedido(conexion)
    tapas = [(1, 1), (2, 2)]  # Tapa 1 x1, Tapa 2 x2
    pedido_id = controlador.crearPedido(usuario_id, tapas)

    # 🔹 Establecer estado a "pendiente"
    cursor.execute("UPDATE pedido SET estado = 'pendiente' WHERE id = %s", (pedido_id,))
    conexion.commit()

    print(f"📦 Pedido de prueba creado con ID: {pedido_id}")

except Exception as e:
    print("❌ Error al crear pedido:", e)

finally:
    conexion.close()
