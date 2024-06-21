import psycopg2

SQL_Tabla_de_Usuarios="CREATE TABLE IF NOT EXISTS USUARIOS (ID serial PRIMARY KEY, USUARIO_NOMBRE VARCHAR(30) NOT NULL, USUARIO_CONTRASEÑA VARCHAR(80) NOT NULL, EMAIL VARCHAR(30))"

class Coneaxion_a_Usuarios:
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

#____________________________________________________________ Sección de usuarios ____________________________________________________________

#Agregar un nuevo usuario (Registro)

def Agreagar_Usuario(Nombre_Usuario, Contraseña_Usuario, Email_Usuario=None):
    DB = Coneaxion_a_Usuarios()
    DB.cursor.execute("SELECT 1 FROM Usuarios WHERE USUARIO_NOMBRE = %s LIMIT 1",(Nombre_Usuario,))
    result = DB.cursor.fetchone()
    if result is None:

        import bcrypt   #Importación de la librería para hashear la contraseña 

        Contraseña_en_bytes =  Contraseña_Usuario.encode('utf-8')   #Encoding de la contraseña en formato bytes
        Contraseña_Hasheada = bcrypt.hashpw(Contraseña_en_bytes, bcrypt.gensalt())   #Hashear la contraseña en formato bytes, en el ingreso a la base de datos de decodea la contraseña para almacenarla en la base de datos
        DB.cursor.execute("INSERT INTO Usuarios (USUARIO_NOMBRE, USUARIO_CONTRASEÑA, EMAIL) VALUES (%s,%s,%s)",(Nombre_Usuario, Contraseña_Hasheada.decode('utf-8'), Email_Usuario))
        DB.cerrar()
        return True
    else:return False

#Verificar usuario (Logeo)

def Validar_Usuario(Nombre_Usuario, Contraseña_Usuario):
    
    import bcrypt

    DB = Coneaxion_a_Usuarios()
    DB.cursor.execute("SELECT USUARIO_NOMBRE,USUARIO_CONTRASEÑA FROM USUARIOS WHERE USUARIO_NOMBRE = %s",(Nombre_Usuario,))
    Verificar = DB.cursor.fetchone()
    if Verificar:
        if bcrypt.checkpw(Contraseña_Usuario.encode('utf-8') , Verificar[1].encode('utf-8') ):
            return True
        else:False
    else:return False

#Buscar usuario

def Buscar_Usuario(Nombre_Usuario):
    DB = Coneaxion_a_Usuarios()
    DB.cursor.execute("SELECT * FROM USUARIOS WHERE USUARIO_NOMBRE = %s", (Nombre_Usuario,))
    return DB.cursor.fetchone()

#Editar usuario

def Editar_Usuario(ID, Nombre_Usuario, Contraseña_Usuario, Email_Usuario=None):
    DB = Coneaxion_a_Usuarios()

    import bcrypt

    Contraseña_en_bytes =  Contraseña_Usuario.encode('utf-8')   #Encoding de la contraseña en formato bytes
    Contraseña_Hasheada = bcrypt.hashpw(Contraseña_en_bytes, bcrypt.gensalt())
    DB.cursor.execute("UPDATE USUARIOS SET USUARIO_NOMBRE = %s, USUARIO_CONTRASEÑA = %s, EMAIL = %s WHERE ID = %s",(Nombre_Usuario, Contraseña_Hasheada.decode('utf-8'), Email_Usuario, ID))
    DB.cerrar()

#Borrar usuario

def Eliminar_Usuario(ID):
    DB = Coneaxion_a_Usuarios()
    DB.cursor.execute("DELETE FROM USUARIOS WHERE ID = %s",(ID,))
    DB.cerrar()
