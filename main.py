import re
import random
from questions import data as questions_data  

def ObtenerRespuesta(entrada_usuario):
    palabras_entrada = re.split(r'\s|[,:;.?!-_]\s*', entrada_usuario.lower())
    respuesta = Revisar_todas_las_respuestas(palabras_entrada)
    return respuesta


def ProbabilidadMensaje(entrada_usuario, palabras_reconocidas, respuesta_unica=False, palabras_requeridas=[]):
    certeza_mensaje = 0
    tiene_palabras_requeridas = True

    for palabra in entrada_usuario:
        if palabra in palabras_reconocidas:
            certeza_mensaje += 1

    porcentaje = float(certeza_mensaje) / float(len(palabras_reconocidas))

    for palabra in palabras_requeridas:
        if palabra not in entrada_usuario:
            tiene_palabras_requeridas = False
            break
    if tiene_palabras_requeridas or respuesta_unica:
        return int(porcentaje * 100)
    else:
        return 0


def Revisar_todas_las_respuestas(mensaje):
    mayor_probabilidad = {}

    def respuesta(respuesta_bot, lista_palabras, respuesta_unica=False, palabras_requeridas=[]):
        nonlocal mayor_probabilidad
        mayor_probabilidad[respuesta_bot] = ProbabilidadMensaje(mensaje, lista_palabras, respuesta_unica, palabras_requeridas)

    for pregunta in questions_data['clients']:  
        respuesta(pregunta['responseBot'], pregunta['listWords'], respuesta_unica=True)

    mejor_coincidencia = max(mayor_probabilidad, key=mayor_probabilidad.get)

    return desconocido() if mayor_probabilidad[mejor_coincidencia] < 1 else mejor_coincidencia


def desconocido():
    respuesta = ['¿Puedes repetir eso?', 'No estoy seguro de lo que quieres decir', 'Intenta buscarlo en Google'][
        random.randrange(3)]
    return respuesta


while True:
    print("Bot: " + ObtenerRespuesta(input('Tú: ')))  

