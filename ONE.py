from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from TWO import *
from typing import Annotated


app_de_FastApi = FastAPI()
app_de_FastApi.mount("/static",StaticFiles(directory="static"),name="static")

Ninja=Jinja2Templates(directory="Templates")

#Registro de usuario ____________________________________________________________________________________________________________________________

@app_de_FastApi.get("/Register", response_class=HTMLResponse)
def Register(request:Request):
    return Ninja.TemplateResponse("Register.html", {"request":request})

@app_de_FastApi.post("/RegisterUser",response_class=RedirectResponse)
def Register_User(UserName:Annotated[str,Form()], PassWord:Annotated[str,Form()], PassWord_Confirm:Annotated[str,Form()]):
    if PassWord == PassWord_Confirm:
        if Agreagar_Usuario(UserName, PassWord):
            return RedirectResponse("/", status_code=303)
        else:
            return RedirectResponse("/Register", status_code=303)
    else:
        return RedirectResponse("/Register", status_code=303)

#Logeo de usuario ____________________________________________________________________________________________________________________________

@app_de_FastApi.get("/Login", response_class=HTMLResponse)
def Login(request:Request):
    return Ninja.TemplateResponse("Login.html", {"request":request})

@app_de_FastApi.post("/LoginUser",response_class=RedirectResponse)
def Login_User(UserName:Annotated[str,Form()], PassWord:Annotated[str,Form()]):
    if Validar_Usuario(UserName, PassWord) == True:
        return RedirectResponse("/", status_code=303)
    else:
        return RedirectResponse("/Login", status_code=303)

#MercadoFree ____________________________________________________________________________________________________________________________

@app_de_FastApi.get("/", response_class=HTMLResponse)
def root(request:Request):
    return Ninja.TemplateResponse("index.html",{"request":request})

@app_de_FastApi.get("/Productos", response_class=HTMLResponse)
def Mostrar_Productos(request:Request):
    return Ninja.TemplateResponse("Productos.html",{"request":request, "Datos":Printear_Todos_los_Datos_del_DB()})

@app_de_FastApi.post("/Productoss", response_class=RedirectResponse)
async def Ingreso_Producto(Nombre_Producto:Annotated[str,Form()],Precio_Producto:Annotated[int,Form()],Descripcion_Producto:Annotated[str,Form()]):
    Agreagar_Producto(Nombre_Producto,Precio_Producto,Descripcion_Producto)
    return RedirectResponse("/Productos", status_code=303)

@app_de_FastApi.get("/Producto_Eliminar", response_class=RedirectResponse)
def Producto_Eliminar(ID:int):
    Borrar_Producto(ID)
    return RedirectResponse("/Productos", status_code=303)

@app_de_FastApi.get("/Editar_Producto", response_class=HTMLResponse)
def Editar_Producto_(ID, request:Request):
    return Ninja.TemplateResponse("Editar_Producto.html",{"request":request, "ID":ID})

@app_de_FastApi.post("/Producto_editado", response_class=RedirectResponse)
def Producto_Editado(ID:Annotated[int,Form()], Nombre_Editado:Annotated[str,Form()],Precio_Editado:Annotated[int,Form()],Descripcion_Editada:Annotated[str,Form()]):
    Editar_Producto(ID, Nombre_Editado, Precio_Editado, Descripcion_Editada)
    return RedirectResponse("/Productos", status_code=303)

@app_de_FastApi.post("/Lista_Buscador", response_class=HTMLResponse)
def Buscar_Producto_en_DB(request:Request,Buscar_Producto_s:Annotated[str,Form()]):
    return Ninja.TemplateResponse("Productos.html",{"request":request, "Datos":Buscar_Producto(Buscar_Producto_s)})