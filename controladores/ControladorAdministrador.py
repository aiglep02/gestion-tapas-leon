class ControladorAdministrador:
    def __init__(self, conexion):
        self.db = conexion

    def obtener_tapas(self):
        cursor = self.db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tapa")
        return cursor.fetchall()

    def insertar_tapa(self, nombre, descripcion, precio, stock):
        cursor = self.db.cursor()
        sql = "INSERT INTO tapa (nombre, descripcion, precio, stock) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (nombre, descripcion, precio, stock))
        self.db.commit()
        return cursor.lastrowid

    def actualizar_tapa(self, tapa_id, nombre=None, descripcion=None, precio=None, stock=None):
        cursor = self.db.cursor()
        sql = "UPDATE tapa SET "
        campos = []
        valores = []

        if nombre:
            campos.append("nombre = %s")
            valores.append(nombre)
        if descripcion:
            campos.append("descripcion = %s")
            valores.append(descripcion)
        if precio is not None:
            campos.append("precio = %s")
            valores.append(precio)
        if stock is not None:
            campos.append("stock = %s")
            valores.append(stock)

        if not campos:
            return 0  # Nada que actualizar

        sql += ", ".join(campos) + " WHERE id = %s"
        valores.append(tapa_id)

        cursor.execute(sql, valores)
        self.db.commit()
        return cursor.rowcount

    def eliminar_tapa(self, tapa_id):
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM tapa WHERE id = %s", (tapa_id,))
        self.db.commit()
        return cursor.rowcount
