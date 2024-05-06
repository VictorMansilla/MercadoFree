import sqlite3
from fastapi import HTTPException

Creation_Base_Data = ('''CREATE TABLE IF NOT EXISTS Productos(
                         ID INTEGER,
                         PRODUCTO_NOMBRE VARCHAR(25),
                         PRECIO INTEGER,
                         DESCRIPCION VARCHAR(500),
                         PRIMARY KEY(ID AUTOINCREMENT)
)''')

class producto:
    def __init__(self,Nombre,Precio,Descripcion):
        self.Nombre = Nombre
        self.Precio = Precio
        self.Descripcion = Descripcion

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

#Agreagar_Producto()

def Agreagar_Producto(Nombre_Producto,Precio_Producto,Descripcion_Producto):
    DB = Coneaxion_a_DB()
    DB.cursor.execute(f"""INSERT OR IGNORE INTO Productos (PRODUCTO_NOMBRE,PRECIO,DESCRIPCION) VALUES ('{Nombre_Producto}','{Precio_Producto}','{Descripcion_Producto}')""")
    DB.cerrar()

#Editar_Producto()

""" def Editar_Producto():
    Preoducto = producto()
    DB = Coneaxion_a_DB()
    #Printear_Todos_los_Datos_del_DB()
    #NOMBRE_PRODUCTO = input('Ingrese el nombre de producto a editar:\n')
    #Elegir_Editar=input('Deseas editar el PRECIO o la DESCRIPCION:\n')
    try:
        if Elegir_Editar.upper()=='PRECIO':
            NUEVO_VALOR=input('Ingrese el nuevo valor:\n')
            DB.cursor.execute(f"UPDATE Productos set PRECIO={NUEVO_VALOR} Where PRODUCTO_NOMBRE like '{NOMBRE_PRODUCTO}'")
        elif Elegir_Editar.upper()=='DESCRIPCION':
            NUEVO_DESCRIPCION=str(input('Ingrese el nueva descripción:\n'))
            DB.cursor.execute(f"UPDATE Productos set DESCRIPCION='{NUEVO_DESCRIPCION}' Where PRODUCTO_NOMBRE like '{NOMBRE_PRODUCTO}'")
        DB.cerrar()
    except:
        print('No se encontro producto') """

#Borrar_Producto()

def Borrar_Producto():
    Preoducto = producto()
    DB = Coneaxion_a_DB()
    #Printear_Todos_los_Datos_del_DB()
    #NOMBRE_PRODUCTO_ELIMINAR = input('Ingrese el nombre de producto a eliminar:\n')
    try:
        DB.cursor.execute(f'DELETE FROM Productos Where PRODUCTO_NOMBRE like "{Preoducto.Nombre}"')
        DB.cerrar()
    except:
        print('No hay productoq ue borrar')

""" elegir = input('ingresar acción: ')
if elegir=='a1':
    Agreagar_Producto()
elif elegir=='a2':
    Editar_Producto()
else:
    Borrar_Producto() """
DB = Coneaxion_a_DB()
DB.cursor.execute(f'DELETE FROM Productos Where ID like "{16}"')
DB.cerrar()