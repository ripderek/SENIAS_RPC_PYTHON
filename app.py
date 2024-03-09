import psycopg2
from jsonrpc import JSONRPCResponseManager, dispatcher
from werkzeug.wrappers import Request, Response
import json
from flask import Flask
from flask_cors import CORS
#imports mapReduce
from multiprocessing import Pool
from collections import defaultdict
import os
import glob
import random
app = Flask(__name__)
CORS(app)
import base64
import os
from datetime import datetime


#NO CAMBIAR LOS NOMBRES DE LAS FUNCIONES, si cambian aqui entonces tambien en el cliente, esto es un RPC no una API 

##############################################SENIAS APP###########################################################
#funcion para recibir las imagenes en JSON y guardarlas en carpetas segun el nombre que se envie skere modo diablo;
#las imagenes se guardan en una carpeta con el nombre de la SENIA que a su vez se encuentra dentro de la carpeta
@dispatcher.add_method
def recibirJsonSenias(nombreSenia, imagenesSenia):
    nombre_carpeta = "./Senias/"+nombreSenia
    if not os.path.exists(nombre_carpeta):
        os.makedirs(nombre_carpeta)
    for imagen in imagenesSenia:
        # Obtener el contenido base64 de la imagen
        contenido_base64 = imagen["img"].split(",")[1]
        # Decodificar el contenido base64
        contenido_bytes = base64.b64decode(contenido_base64)
        fecha_actual = datetime.now().strftime("%Y%m%d%H%M%S") #para evitar que se puedan repetir
        with open(os.path.join(nombre_carpeta, f"{imagen['id']}_{fecha_actual}.png"), "wb") as archivo:
            archivo.write(contenido_bytes)

#Funcion vacia para darle la funcionalidad de generar el modelo 
@dispatcher.add_method
def GenerarModelo():
    #EN LA BD GUARDAR TAMBIEN EL NOMBRE DEL MODELO PARA LUEGO ADMINISTRARLO
    print("AQUI GENERAR EL MODELO Y GUARDARLO EN UNA CARPETA DONDE SE ENCUENTREN TODOS LOS MODELOS CON EL NOMBRE POR FECHA")
    #La carpeta principal puede ser: ./Modelo/ y dentro tendrian que ir los modelos generados con la fecha como nombre

#if __name__ == "__main__":
 #   app.run(host='0.0.0.0', port=81)

@Request.application
def application(request):
    response = JSONRPCResponseManager.handle(
        request.get_data(as_text=True),
        dispatcher
    )
    #Aun no tiene la funcion de los tokens y creo que es mejor de momento skere
    # Configuración de los encabezados CORS
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
    }
    return Response(response.json, content_type='application/json', headers=headers)

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('localhost', 4000, application)