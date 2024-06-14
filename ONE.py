from fastapi import FastAPI, HTTPException
import jwt

from database.Database_Product import Printear_Todos_los_Datos_del_DB, Printear_un_Producto, Agreagar_Producto, Borrar_Producto, Editar_Producto, Buscar_Producto, Printear_Mis_Productos
from database.Database_User import  Agreagar_Usuario, Validar_Usuario, Editar_Usuario, Eliminar_Usuario
from api.encode import Token,second_exp,Clave_Secreta

app_de_FastApi = FastAPI()

lista_carrito=[] #Lista de productos demandados por el usuario

#Registro de usuario ____________________________________________________________________________________________________________________________

@app_de_FastApi.post("/Register")
def Register_User(UserName:str, PassWord:str, PassWord_Confirm:str, Email=None):
    if PassWord == PassWord_Confirm:
        if Agreagar_Usuario(UserName, PassWord, Email):
            raise HTTPException(
            status_code=201,
            detail="Usuario ingresado",
            headers={"WWW-Authenticate": "Bearer"},)
        else:
            raise HTTPException(
            status_code=404,
            detail="El usuario ya está registrado",
            headers={"WWW-Authenticate": "Bearer"},)
    else:
        raise HTTPException(
            status_code=400,
            detail="Las contraseñas no coinciden",
            headers={"WWW-Authenticate": "Bearer"},)

#Logeo de usuario ____________________________________________________________________________________________________________________________

@app_de_FastApi.get("/Login")
def Login_User(UserName:str, PassWord:str):
    if Validar_Usuario(UserName, PassWord):
        return Token(UserName, second_exp)
    else:
        raise HTTPException(
        status_code=404,
        detail="Usuario o contraseña incorrectas",            
        headers={"WWW-Authenticate": "Bearer"},)

@app_de_FastApi.get("/LogOut")
def LogOut():
    headers={"set-cookie": "acces_token=; Max-Age=0"}
    return headers

#Eliminación de usuario ____________________________________________________________________________________________________________________________

@app_de_FastApi.delete("/DeleteUser")
def Delete_User(UserName:str, PassWord:str, acces_token):
    try:
        decoded_payload = jwt.decode(acces_token, Clave_Secreta, algorithms=['HS256'])

        if Validar_Usuario(UserName, PassWord):
            Eliminar_Usuario(UserName)

        else:
            raise HTTPException(
                status_code=404,
                detail="Usuario o contraseña incorrectas",            
                headers={"WWW-Authenticate": "Bearer"},)

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="El token ha expirado",
            headers={"WWW-Authenticate": "Bearer"},)

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},)

#Eliminación de usuario ____________________________________________________________________________________________________________________________

@app_de_FastApi.put("/Editar_Usuario", status_code=201)
def Usuario_Editar(UserName:str, PassWord:str, acces_token, Email:str|None=None):
    try:
        decoded_payload = jwt.decode(acces_token, Clave_Secreta, algorithms=['HS256'])

        if acces_token != None:
            Editar_Usuario(decoded_payload['Id_Usuario'], UserName, PassWord, Email)

        else:
            raise HTTPException(
                status_code = 400,
                detail="Cookie invalida",
                headers={"WWW-Authenticate": "Bearer"},)

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="El token ha expirado",
            headers={"WWW-Authenticate": "Bearer"},)

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},)

#MercadoFree ____________________________________________________________________________________________________________________________

@app_de_FastApi.get("/Productos")
def Productos_Mostrar(acces_token:str|None=None):
    if acces_token == None:
        raise HTTPException(
            status_code = 400,
            detail="Cookie invalida",
            headers={"WWW-Authenticate": "Bearer"},)
    else:
        return Printear_Todos_los_Datos_del_DB()

@app_de_FastApi.post("/Productos", status_code= 201)
async def Producto_Ingresar(Nombre_Producto:str, Precio_Producto:int, Descripcion_Producto:str, acces_token:str|None=None):
    try:
        decoded_payload = jwt.decode(acces_token, Clave_Secreta, algorithms=['HS256'])
        print(f'Token decodificado: {decoded_payload}')
        if acces_token == None:
            raise HTTPException(
                status_code = 400,
                detail="Cookie invalida",
                headers={"WWW-Authenticate": "Bearer"},)
        else:
            Agreagar_Producto(Nombre_Producto,Precio_Producto,Descripcion_Producto, decoded_payload['Id_Usuario'])

    except jwt.ExpiredSignatureError:
        print('El token ha expirado')
        raise HTTPException(
            status_code=401,
            detail="El token ha expirado",
            headers={"WWW-Authenticate": "Bearer"},)

    except jwt.InvalidTokenError:
        print('Token inválido')
        raise HTTPException(
            status_code=401,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},)

@app_de_FastApi.delete("/Producto_Eliminar", status_code=204)
async def Producto_Eliminar(ID:int, acces_token:str|None=None):
    if acces_token != None:
        try:
            decoded_payload = jwt.decode(acces_token, Clave_Secreta, algorithms=['HS256'])
            print(f'Token decodificado: {decoded_payload}')
            Borrar_Producto(ID)

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=401,
                detail="El token ha expirado",
                headers={"WWW-Authenticate": "Bearer"},)

        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=401,
                detail="Token inválido",
                headers={"WWW-Authenticate": "Bearer"},)
    else:
        raise HTTPException(
            status_code = 400,
            detail="Cookie invalida",
            headers={"WWW-Authenticate": "Bearer"},)

@app_de_FastApi.put("/Editar_Producto")
def Producto_Editar(ID, Nombre_Producto, Precio_Producto, Descripcion_Producto, acces_token):
    try:
        decoded_payload = jwt.decode(acces_token, Clave_Secreta, algorithms=['HS256'])
        if acces_token == None:
            raise HTTPException(
                status_code = 400,
                detail="Cookie invalida",
                headers={"WWW-Authenticate": "Bearer"},)
        else:
            Editar_Producto(ID, Nombre_Producto, Precio_Producto, Descripcion_Producto)

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="El token ha expirado",
            headers={"WWW-Authenticate": "Bearer"},)

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},)

@app_de_FastApi.get("/Lista_Buscador")
def Buscar_Producto_en_DB(Buscar_Producto_s:str):
    return Buscar_Producto(Buscar_Producto_s)

@app_de_FastApi.get("/Producto")
def Producto(ID:int):
    return Printear_un_Producto(ID)

@app_de_FastApi.get("/MisProductos")
def MisProductos(acces_token):
    decoded_payload = jwt.decode(acces_token, Clave_Secreta, algorithms=['HS256'])
    return Printear_Mis_Productos(decoded_payload['Id_Usuario'])

@app_de_FastApi.post("/Carrito")
def carrito(ID:int):
    lista_carrito.append(ID)

@app_de_FastApi.get("/Carritototal")
def Total_Carrito():
    total = 0
    for x in lista_carrito:
        P:str = Printear_un_Producto(x)
        total+=P[2]
    return f"{lista_carrito}", f"{total}"