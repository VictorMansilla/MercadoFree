import psycopg2
from psycopg2 import sql

SQL_Tabla_de_Produuctos="CREATE TABLE IF NOT EXISTS PRODUCTOS (ID serial PRIMARY KEY, PRODUCTO_NOMBRE VARCHAR(30), PRECIO INTEGER, DESCRIPCION VARCHAR(200))"

SQL_Tabla_de_Usuarios="CREATE TABLE IF NOT EXISTS USUARIOS (ID serial PRIMARY KEY, USUARIO_NOMBRE VARCHAR(30), USUARIO_CONTRASEÑA VARCHAR(30))"

class Coneaxion_a_DB_Productos:
    def __init__(self):
        self.conn = psycopg2.connect(dbname="Aprendizaje",
                                     user="Soporte",
                                     password="Soporte",
                                     host="localhost",
                                     port="5432")
        self.cursor = self.conn.cursor()
        self.cursor.execute(SQL_Tabla_de_Produuctos)
        self.conn.commit()

    def cerrar(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

class Coneaxion_a_Usuarios():
    def __init__(self):
        self.conn = psycopg2.connect(dbname="Aprendizaje",
                                     user="Soporte",
                                     password="Soporte",
                                     host="localhost",
                                     port="5432")
        self.cursor = self.conn.cursor()
        self.cursor.execute(SQL_Tabla_de_Usuarios)
        self.conn.commit()

    def cerrar(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

#____________________________________________________________ Sección de productos ____________________________________________________________

def Printear_Todos_los_Datos_del_DB():
    DB = Coneaxion_a_DB_Productos()
    DB.cursor.execute("SELECT * FROM PRODUCTOS")
    return DB.cursor.fetchall()

def Printear_un_Producto(ID):
    DB = Coneaxion_a_DB_Productos()
    DB.cursor.execute("SELECT * FROM productos WHERE ID = %s", (ID,))
    return DB.cursor.fetchone()

#Agreagar un nuevo producto

def Agreagar_Producto(Nombre_Producto,Precio_Producto,Descripcion_Producto):
    DB = Coneaxion_a_DB_Productos()
    DB.cursor.execute("INSERT INTO PRODUCTOS (PRODUCTO_NOMBRE,PRECIO,DESCRIPCION) VALUES (%s,%s,%s)",(Nombre_Producto,Precio_Producto,Descripcion_Producto))
    DB.cerrar()

#Borrar el producto seleccionado

def Borrar_Producto(ID):
    DB = Coneaxion_a_DB_Productos()
    DB.cursor.execute("DELETE FROM PRODUCTOS WHERE ID = %s",(ID,))
    DB.cerrar()

#Editar un producto seleccionado

def Editar_Producto(ID, Nombre_Editado, Precio_Editado, Descripcion_Editada):
    DB = Coneaxion_a_DB_Productos()
    DB.cursor.execute("UPDATE PRODUCTOS SET PRODUCTO_NOMBRE = %s, PRECIO = %s, DESCRIPCION = %s WHERE ID = %s",(Nombre_Editado, Precio_Editado, Descripcion_Editada,ID))
    DB.cerrar()

#Buscar los productos

def Buscar_Producto(Buscar_Producto_s):
    DB = Coneaxion_a_DB_Productos()
    query = "SELECT * FROM Productos WHERE PRODUCTO_NOMBRE ILIKE %s"
    DB.cursor.execute(query, ('%' + Buscar_Producto_s + '%',))
    return DB.cursor.fetchall()

#____________________________________________________________ Sección de usuarios ____________________________________________________________

#Agregar un nuevo usuario (Registro)

def Agreagar_Usuario(Nombre_Usuario, Contraseña_Usuario):
    DB = Coneaxion_a_Usuarios()
    DB.cursor.execute("SELECT 1 FROM Usuarios WHERE USUARIO_NOMBRE = %s LIMIT 1",(Nombre_Usuario,))
    result = DB.cursor.fetchone()
    if result == None:
        DB.cursor.execute("INSERT INTO Usuarios (USUARIO_NOMBRE,USUARIO_CONTRASEÑA) VALUES (%s,%s)",(Nombre_Usuario,Contraseña_Usuario))
        DB.cerrar()
        return True
    else:return False

#Verificar usuario (Logeo)

def Validar_Usuario(Nombre_Usuario, Contraseña_Usuario):
    DB = Coneaxion_a_Usuarios()
    DB.cursor.execute("SELECT * FROM USUARIOS WHERE USUARIO_NOMBRE = %s AND USUARIO_CONTRASEÑA = %s",(Nombre_Usuario,Contraseña_Usuario))
    Verificar = DB.cursor.fetchone()
    if Verificar:
        return True
    else:return False