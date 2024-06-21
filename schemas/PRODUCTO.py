from pydantic import BaseModel

class PRODUCTO_BASE(BaseModel):
    NOMBRE : str
    PRECIO : int
    DESCRIPCION : str