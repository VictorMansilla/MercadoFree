import secrets
import jwt
import datetime


from database.Database_User import Buscar_Usuario


Clave_Secreta = secrets.token_hex(62)

second_exp = 120

def Token(Nombre_Usuario, segundos):
    Usuario = Buscar_Usuario(Nombre_Usuario)
    payload = {
        'Id_Usuario': Usuario[0],
        'Nombre_Usuario': Usuario[1],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=segundos)}
    token = jwt.encode(payload, Clave_Secreta, algorithm='HS256')
    return token
