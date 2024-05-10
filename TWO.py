import sqlite3

Creation_Base_Data = ('''CREATE TABLE IF NOT EXISTS Productos(
                         ID INTEGER,
                         PRODUCTO_NOMBRE VARCHAR(25),
                         PRECIO INTEGER,
                         DESCRIPCION VARCHAR(500),
                         PRIMARY KEY(ID AUTOINCREMENT)
)''')

""" class producto:
    def __init__(self,Nombre,Precio,Descripcion):
        self.Nombre = Nombre
        self.Precio = Precio
        self.Descripcion = Descripcion """

class Coneaxion_a_DB:
    def __init__(self):
        self.base_datos = 'C:\\Users\\User\\Desktop\\tarea\\PYtrabajo\\BANGA\\Base_Datos_Productos.db'
        self.conexion = sqlite3.connect(self.base_datos)
        self.cursor = self.conexion.cursor()

    def cerrar(self):
        self.conexion.commit()
        self.conexion.close()

def Printear_Todos_los_Datos_del_DB():
    DB = Coneaxion_a_DB()
    DB.cursor.execute("SELECT * FROM Productos")
    return DB.cursor.fetchall()

#Agreagar un nuevo producto

def Agreagar_Producto(Nombre_Producto,Precio_Producto,Descripcion_Producto):
    DB = Coneaxion_a_DB()
    DB.cursor.execute(f"""INSERT OR IGNORE INTO Productos (PRODUCTO_NOMBRE,PRECIO,DESCRIPCION) VALUES ('{Nombre_Producto}','{Precio_Producto}','{Descripcion_Producto}')""")
    DB.cerrar()

#Borrar el producto seleccionado

def Borrar_Producto(ID):
    DB = Coneaxion_a_DB()
    DB.cursor.execute(f'DELETE FROM Productos Where ID like "{ID}"')
    DB.cerrar()

#Editar un producto seleccionado

def Editar_Producto(ID, Nombre_Editado, Precio_Editado, Descripcion_Editada):
    DB = Coneaxion_a_DB()
    DB.cursor.execute(f'UPDATE Productos SET PRODUCTO_NOMBRE="{Nombre_Editado}", PRECIO={Precio_Editado}, DESCRIPCION="{Descripcion_Editada}" WHERE ID="{ID}"')
    DB.cerrar()