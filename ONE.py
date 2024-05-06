from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from TWO import *

from typing import Annotated, Union

from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

app_de_FastApi = FastAPI()

Ninja=Jinja2Templates(directory="Templates")

@app_de_FastApi.get("/", response_class=HTMLResponse)
def root(request:Request):
    return Ninja.TemplateResponse("index.html",{"request":request})

@app_de_FastApi.get("/dashboard",response_class=HTMLResponse)
def Dashboard(request:Request):
    return Ninja.TemplateResponse("dashboard.html", {"request": request})

@app_de_FastApi.post("/Productoss")
async def Ingreso_Producto(Nombre_Producto:Annotated[str,Form()],Precio_Producto:Annotated[int,Form()],Descripcion_Producto:Annotated[str,Form()]):
    Agreagar_Producto(Nombre_Producto,Precio_Producto,Descripcion_Producto)
    return RedirectResponse("/Productos", status_code=303)

@app_de_FastApi.get("/Productos",response_class=HTMLResponse)
def Mostrar_Productos(request:Request):
    return Ninja.TemplateResponse("Productos.html",{"request":request, "Datos":Printear_Todos_los_Datos_del_DB()})


""" @app_de_FastApi.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app_de_FastApi.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id} """