from controladores.ControladorPedido import ControladorPedido
from modelos.ConexionMYSQL import ConexionMYSQL

conexion = ConexionMYSQL().conexion

try:
    cursor = conexion.cursor()

    # 1. Insertar tapas si no existen
    cursor.execute("SELECT COUNT(*) FROM tapa WHERE id IN (1, 2)")
    tapas_existentes = cursor.fetchone()[0]
    if tapas_existentes < 2:
        cursor.execute("INSERT INTO tapa (id, nombre, descripcion, precio, stock) VALUES (1, 'Tortilla', 'Con cebolla', 2.5, 10)")
        cursor.execute("INSERT INTO tapa (id, nombre, descripcion, precio, stock) VALUES (2, 'Chorizo', 'Picante', 2.0, 8)")
        print("✅ Tapas de prueba insertadas.")
    conexion.commit()

    # 2. Insertar usuario
    cursor.execute("""
        INSERT INTO usuario (nombre, email, contraseña, rol)
        VALUES ('UsuarioReal', 'real@correo.com', '1234', 'cliente')
    """)
    conexion.commit()

    cursor.execute("SELECT LAST_INSERT_ID()")
    usuario_id = cursor.fetchone()[0]
    print(f"Usuario insertado con ID: {usuario_id}")

    # 3. Crear pedido
    controlador = ControladorPedido(conexion)
    tapas = [(1, 1), (2, 2)]  # Tapa 1 x1, tapa 2 x2
    pedido_id = controlador.crearPedido(usuario_id, tapas)
    conexion.commit()

    print(f"Pedido insertado con ID: {pedido_id}")

except Exception as e:
    print("Error:", e)

finally:
    conexion.close()
    print("Conexión cerrada.")





    
