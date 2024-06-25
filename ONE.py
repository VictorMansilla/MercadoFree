from fastapi import FastAPI, HTTPException, Depends
import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from models.Database_Product import Printear_Todos_los_Datos_del_DB, Printear_un_Producto, Agreagar_Producto, Borrar_Producto, Editar_Producto, Buscar_Producto, Printear_Mis_Productos
from models.Database_User import  Agreagar_Usuario, Validar_Usuario, Editar_Usuario, Eliminar_Usuario
from api.encode import Token,second_exp,Clave_Secreta, algoritmo
from schemas.USUARIO import USUARIO_BASE, USUARIO_EMAIL
from schemas.PRODUCTO import PRODUCTO_BASE

app_de_FastApi = FastAPI()

lista_carrito=[] #Lista de productos demandados por el usuario

esquema_oauth2 = OAuth2PasswordBearer(tokenUrl="Login")

def Excepcion(codigo_de_estado : int, detalle : str):
    raise HTTPException(status_code = codigo_de_estado, detail = detalle)

#Registro de usuario ____________________________________________________________________________________________________________________________

@app_de_FastApi.post("/Register", response_model = USUARIO_BASE)
def Register_User(Usuario : USUARIO_EMAIL, PassWord_Confirm:str):
    if Usuario.CONTRASEÑA == PassWord_Confirm:
        if Agreagar_Usuario(Usuario.NOMBRE, Usuario.CONTRASEÑA):
            Excepcion(201, "Usuario ingresado")
        
        else:
            Excepcion(404, "El usuario ya está registrado")
        
    else:
        Excepcion(400, "Las contraseñas no coinciden")
    
#Logeo de usuario ____________________________________________________________________________________________________________________________

@app_de_FastApi.post("/Login")   ##########################################################
def Login_User(Oauth : OAuth2PasswordRequestForm = Depends()):
    if Validar_Usuario(Oauth.username, Oauth.password):
        acces_token = Token(Oauth.username, second_exp)
        return {"access_token": acces_token, "token_type": "bearer"}

    else:
        Excepcion(404, "Usuario o contraseña incorrectas")

@app_de_FastApi.get("/LogOut")
def LogOut():
    headers={"set-cookie": "acces_token=; Max-Age=0"}
    return headers

#Eliminación de usuario ____________________________________________________________________________________________________________________________

@app_de_FastApi.delete("/DeleteUser")   ##########################################################
async def Delete_User(Usuario : USUARIO_BASE, acces_token : str = Depends(esquema_oauth2)):
    try:
        decoded_payload = jwt.decode(acces_token, Clave_Secreta, algorithms=algoritmo)

        if Validar_Usuario(Usuario.NOMBRE, Usuario.CONTRASEÑA):
            Eliminar_Usuario(decoded_payload['Id_Usuario'])

        else:
            Excepcion(404, "Usuario o contraseña incorrectas")

    except jwt.ExpiredSignatureError:
        Excepcion(401, "El token ha expirado")

    except jwt.InvalidTokenError:
        Excepcion(401, "Token inválido")

#Eliminación de usuario ____________________________________________________________________________________________________________________________

@app_de_FastApi.put("/Editar_Usuario", status_code = 201)   ##########################################################
async def Edit_User(Usuario : USUARIO_EMAIL, acces_token : str = Depends(esquema_oauth2)):
    try:
        decoded_payload = jwt.decode(acces_token, Clave_Secreta, algorithms=algoritmo)

        if acces_token != None:
            Editar_Usuario(decoded_payload['Id_Usuario'], Usuario.NOMBRE, Usuario.CONTRASEÑA, Usuario.EMAIL)

        else:
            Excepcion(400, "Cookie invalida")

    except jwt.ExpiredSignatureError:
        Excepcion(401, "El token ha expirado")

    except jwt.InvalidTokenError:
        Excepcion(401, "Token inválido")

#MercadoFree ____________________________________________________________________________________________________________________________

@app_de_FastApi.get("/Productos")
def Show_Products(acces_token:str|None=None):
    if acces_token == None:
            Excepcion(400, "Cookie invalida")

    else:
        return Printear_Todos_los_Datos_del_DB()

@app_de_FastApi.post("/Productos", status_code = 201)   ##########################################################
async def Product_Get_Into(Producto : PRODUCTO_BASE, acces_token : str = Depends(esquema_oauth2)):
    try:
        decoded_payload = jwt.decode(acces_token, Clave_Secreta, algorithms=algoritmo)

        if acces_token == None:
            Excepcion(400, "Cookie invalida")
            
        else:
            Agreagar_Producto(Producto.NOMBRE, Producto.PRECIO, Producto.DESCRIPCION, decoded_payload['Id_Usuario'])

    except jwt.ExpiredSignatureError:
        Excepcion(401, "El token ha expirado")

    except jwt.InvalidTokenError:
        Excepcion(401, "Token inválido")

@app_de_FastApi.delete("/Producto_Eliminar", status_code=204)   ##########################################################
async def Product_Delet(ID : int, acces_token : str = Depends(esquema_oauth2)):
    if acces_token != None:
        try:
            decoded_payload = jwt.decode(acces_token, Clave_Secreta, algorithms=algoritmo)
            Borrar_Producto(ID, decoded_payload['Id_Usuario'])

        except jwt.ExpiredSignatureError:
            Excepcion(401, "El token ha expirado")

        except jwt.InvalidTokenError:
            Excepcion(401, "Token inválido")
        
    else:
        raise HTTPException(
            status_code = 400,
            detail="Cookie invalida")

@app_de_FastApi.put("/Editar_Producto")   ##########################################################
def Product_Editr(ID : int, Producto : PRODUCTO_BASE, acces_token : str = Depends(esquema_oauth2)):
    try:
        decoded_payload = jwt.decode(acces_token, Clave_Secreta, algorithms=algoritmo)
        if acces_token == None:
            Excepcion(400, "Cookie invalida")

        else:
            Editar_Producto(ID, Producto.NOMBRE, Producto.PRECIO, Producto.DESCRIPCION, decoded_payload['Id_Usuario'])

    except jwt.ExpiredSignatureError:
        Excepcion(401, "El token ha expirado")

    except jwt.InvalidTokenError:
            Excepcion(401, "Token inválido")

@app_de_FastApi.get("/Lista_Buscador")
def Search_Product_in_DB(Buscar_Producto_s:str):
    return Buscar_Producto(Buscar_Producto_s)

@app_de_FastApi.get("/Productos/{ID}") 
def Product(ID : int):
    return Printear_un_Producto(ID)

@app_de_FastApi.get("/MisProductos")
def My_Products(acces_token):
    decoded_payload = jwt.decode(acces_token, Clave_Secreta, algorithms=algoritmo)
    return Printear_Mis_Productos(decoded_payload['Id_Usuario'])

@app_de_FastApi.post("/Carrito")
def Cart(ID:int):
    lista_carrito.append(ID)

@app_de_FastApi.get("/Carritototal")
def Total_Cart():
    total = 0
    for x in lista_carrito:
        P:str = Printear_un_Producto(x)
        total+=P[2]
    return f"{lista_carrito}", f"{total}"

@app_de_FastApi.post("/Pagar")
def Pay(Numero_Tarjeta : int, Tres_Digitos : int, acces_token):
    try:
        decoded_payload = jwt.decode(acces_token, Clave_Secreta, algorithms=algoritmo)

        if acces_token != None:
            total = 0
            for x in lista_carrito:
                P:str = Printear_un_Producto(x)
                total+=P[2]
            return f"El total pagado es {total}"
        else:
            Excepcion(400, "Cookie invalida")

    except jwt.ExpiredSignatureError:
        Excepcion(401, "El token ha expirado")

    except jwt.InvalidTokenError:
            Excepcion(401, "Token inválido")
