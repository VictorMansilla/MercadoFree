import jwt
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

from models.Database_User import Buscar_Usuario


Clave_Secreta = os.getenv('clave_secreta')

second_exp = int(os.getenv('segundos_exp'))

algoritmo:list = [os.getenv('algoritmo')]

def Token(Nombre_Usuario, segundos):
    Usuario = Buscar_Usuario(Nombre_Usuario)
    payload = {
        'Id_Usuario': Usuario[0],
        'Nombre_Usuario': Usuario[1],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=segundos)}
    token = jwt.encode(payload, Clave_Secreta, algorithm=os.getenv('algoritmo'))
    return token