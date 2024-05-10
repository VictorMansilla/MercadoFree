from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from TWO import *
from typing import Annotated

app_de_FastApi = FastAPI()
app_de_FastApi.mount("/static",StaticFiles(directory="static"),name="static")

Ninja=Jinja2Templates(directory="Templates")

@app_de_FastApi.get("/", response_class=HTMLResponse)
def root(request:Request):
    return Ninja.TemplateResponse("index.html",{"request":request})

@app_de_FastApi.get("/Productos",response_class=HTMLResponse)
def Mostrar_Productos(request:Request):
    return Ninja.TemplateResponse("Productos.html",{"request":request, "Datos":Printear_Todos_los_Datos_del_DB()})

@app_de_FastApi.post("/Productoss", response_class=RedirectResponse)
def Ingreso_Producto(Nombre_Producto:Annotated[str,Form()],Precio_Producto:Annotated[int,Form()],Descripcion_Producto:Annotated[str,Form()]):
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