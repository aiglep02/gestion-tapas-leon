class ControladorTapa:
    def __init__(self, conexion):
        self.db = conexion

    def obtener_tapas(self):
        cursor = self.db.cursor(dictionary=True)
        cursor.execute("SELECT id, nombre, descripcion, precio, stock FROM tapa")
        return cursor.fetchall()

    def insertar_tapa(self, nombre, descripcion, precio, stock):
        cursor = self.db.cursor()
        sql = "INSERT INTO tapa (nombre, descripcion, precio, stock) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (nombre, descripcion, precio, stock))
        self.db.commit()
        return cursor.lastrowid

    def eliminar_tapa(self, tapa_id):
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM tapa WHERE id = %s", (tapa_id,))
        self.db.commit()

    def actualizar_stock(self, tapa_id, nuevo_stock):
        cursor = self.db.cursor()
        cursor.execute("UPDATE tapa SET stock = %s WHERE id = %s", (nuevo_stock, tapa_id))
        self.db.commit()
