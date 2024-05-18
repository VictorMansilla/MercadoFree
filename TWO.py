import sqlite3

#Base de datos de productos

Creation_Base_Data = ('''CREATE TABLE IF NOT EXISTS Productos(
                         ID INTEGER,
                         PRODUCTO_NOMBRE VARCHAR(25),
                         PRECIO INTEGER,
                         DESCRIPCION VARCHAR(500),
                         PRIMARY KEY(ID AUTOINCREMENT))''')

#Base de datos de usuarios

Creation_Base_Data_Usuarios = ('''CREATE TABLE IF NOT EXISTS Usuarios(
                      ID INTEGER,
                      USUARIO_NOMBRE VARCHAR(25),
                      USUARIO_CONTRASEÑA VARCHAR(50),
                      PRIMARY KEY(ID AUTOINCREMENT))''')

class Coneaxion_a_DB_Productos:
    def __init__(self):
        self.base_datos_productos = 'C:\\Users\\User\\Desktop\\tarea\\PYtrabajo\\BANGA\\Base_Datos_Productos.db'
        self.conexion = sqlite3.connect(self.base_datos_productos)
        self.conexion.execute(Creation_Base_Data)
        self.cursor = self.conexion.cursor()

    def cerrar(self):
        self.conexion.commit()
        self.conexion.close()

#____________________________________________________________ Sección de productos ____________________________________________________________

def Printear_Todos_los_Datos_del_DB():
    DB = Coneaxion_a_DB_Productos()
    DB.cursor.execute("SELECT * FROM Productos")
    return DB.cursor.fetchall()

#Agreagar un nuevo producto

def Agreagar_Producto(Nombre_Producto,Precio_Producto,Descripcion_Producto):
    DB = Coneaxion_a_DB_Productos()
    DB.cursor.execute(f'INSERT OR IGNORE INTO Productos (PRODUCTO_NOMBRE,PRECIO,DESCRIPCION) VALUES ("{Nombre_Producto}","{Precio_Producto}","{Descripcion_Producto}")')
    DB.cerrar()

#Borrar el producto seleccionado

def Borrar_Producto(ID):
    DB = Coneaxion_a_DB_Productos()
    DB.cursor.execute(f'DELETE FROM Productos Where ID like "{ID}"')
    DB.cerrar()

#Editar un producto seleccionado

def Editar_Producto(ID, Nombre_Editado, Precio_Editado, Descripcion_Editada):
    DB = Coneaxion_a_DB_Productos()
    DB.cursor.execute(f'UPDATE Productos SET PRODUCTO_NOMBRE="{Nombre_Editado}", PRECIO={Precio_Editado}, DESCRIPCION="{Descripcion_Editada}" WHERE ID="{ID}"')
    DB.cerrar()

#Buscar los productos

def Buscar_Producto(Buscar_Producto_s):
    DB = Coneaxion_a_DB_Productos()
    DB.cursor.execute(f"SELECT * FROM Productos WHERE PRODUCTO_NOMBRE LIKE '{Buscar_Producto_s}'")
    return DB.cursor.fetchall()

#____________________________________________________________ Sección de usuarios ____________________________________________________________

class Coneaxion_a_Usuarios():
    def __init__(self):
        self.base_datos_usuarios = 'C:\\Users\\User\\Desktop\\tarea\\PYtrabajo\\BANGA\\Base_Datos_Usuarios.db'
        self.conexion = sqlite3.connect(self.base_datos_usuarios)
        self.conexion.execute(Creation_Base_Data_Usuarios)
        self.cursor = self.conexion.cursor()
    
    def cerrar(self):
        self.conexion.commit()
        self.conexion.close()
    
#Agregar un nuevo usuario (Registro)

def Agreagar_Usuario(Nombre_Usuario, Contraseña_Usuario):
    DB = Coneaxion_a_Usuarios()
    DB.cursor.execute(f'SELECT 1 FROM Usuarios WHERE USUARIO_NOMBRE="{Nombre_Usuario}" LIMIT 1')
    result = DB.cursor.fetchone()
    if result == None:
        DB.cursor.execute(f'INSERT OR IGNORE INTO Usuarios (USUARIO_NOMBRE,USUARIO_CONTRASEÑA) VALUES ("{Nombre_Usuario}","{Contraseña_Usuario}")')
        DB.cerrar()
        return True
    else:return False

#Verificar usuario (Logeo)

def Validar_Usuario(Nombre_Usuario, Contraseña_Usuario):
    DB = Coneaxion_a_Usuarios()
    DB.cursor.execute(f'SELECT * FROM Usuarios WHERE USUARIO_NOMBRE="{Nombre_Usuario}" AND USUARIO_CONTRASEÑA="{Contraseña_Usuario}"')
    Verificar = DB.cursor.fetchall()
    if Verificar:
        return True
    else:return False


""" DB = Coneaxion_a_Usuarios()
DB.cursor.execute(f'DELETE FROM Usuarios Where USUARIO_NOMBRE like "{"victor"}"')
DB.cerrar() """