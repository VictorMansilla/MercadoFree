from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from TWO import *

from typing import Annotated

app_de_FastApi = FastAPI()

Ninja=Jinja2Templates(directory="Templates")

@app_de_FastApi.get("/", response_class=HTMLResponse)
def root(request:Request):
    return Ninja.TemplateResponse("index.html",{"request":request})

@app_de_FastApi.get("/dashboard",response_class=HTMLResponse)
def Dashboard(request:Request):
    return Ninja.TemplateResponse("dashboard.html", {"request": request})

@app_de_FastApi.post("/Productos")
def Ingreso_Producto(Nombre_Producto:Annotated[str,Form()],Precio_Producto:Annotated[int,Form()],Descripcion_Producto:Annotated[str,Form()]):
    #Agreagar_Producto(Nombre_Producto,Precio_Producto,Descripcion_Producto)
    #datos = Printear_Todos_los_Datos_del_DB()
    return {"nombre del Producto": Nombre_Producto,
            "Precio":Precio_Producto,
            "Descripción":Descripcion_Producto}, Printear_Todos_los_Datos_del_DB()