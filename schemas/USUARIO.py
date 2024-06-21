from pydantic import BaseModel
from typing import Union

class USUARIO_BASE(BaseModel):
    NOMBRE : str
    CONTRASEÑA : str

class USUARIO_EMAIL(USUARIO_BASE):
    EMAIL : Union[str, None] = None