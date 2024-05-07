from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from TWO import *
from typing import Annotated, Union
#from pydantic import BaseModel

app_de_FastApi = FastAPI()
app_de_FastApi.mount("/static",StaticFiles(directory="static"),name="static")

Ninja=Jinja2Templates(directory="Templates")

@app_de_FastApi.get("/", response_class=HTMLResponse)
def root(request:Request):
    return Ninja.TemplateResponse("index.html",{"request":request})

@app_de_FastApi.get("/dashboard",response_class=HTMLResponse)
def Dashboard(request:Request):
    return Ninja.TemplateResponse("dashboard.html", {"request": request})

@app_de_FastApi.post("/Productoss", response_class=RedirectResponse)
async def Ingreso_Producto(Nombre_Producto:Annotated[str,Form()],Precio_Producto:Annotated[int,Form()],Descripcion_Producto:Annotated[str,Form()]):
    Agreagar_Producto(Nombre_Producto,Precio_Producto,Descripcion_Producto)
    return RedirectResponse("/Productos", status_code=303)

@app_de_FastApi.get("/Productos",response_class=HTMLResponse)
def Mostrar_Productos(request:Request):
    return Ninja.TemplateResponse("Productos.html",{"request":request, "Datos":Printear_Todos_los_Datos_del_DB()})

@app_de_FastApi.delete("/Producto_Eliminar", response_class=RedirectResponse)
async def Producto_Eliminar(ID:Annotated[int,Form()]):
    Borrar_Producto(ID)
    return RedirectResponse("/Productos", status_code=303)