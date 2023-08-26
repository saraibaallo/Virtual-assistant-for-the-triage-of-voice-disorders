"""
Código que dadas las respuestas del paciente, las guarda en el historial, generando el fichero correspondiente.
"""

#coding utp-8

import os
from datetime import datetime
from cryptography.fernet import Fernet

def obtener_SO():
    so = os.name
    if so == "nt":
        caracter = "\\"
    elif so == "posix":
        caracter = "/"
    return caracter

def obtener_key():
    carpeta = "filekey"
    caracter = obtener_SO()
    if not os.path.exists(carpeta):
        os.mkdir(carpeta)
        key = Fernet.generate_key()
        with open(f'{carpeta}{caracter}filekey.key', 'wb') as filekey:
            filekey.write(key)
    else:
        with open(f'{carpeta}{caracter}filekey.key', 'rb') as filekey:
            key = filekey.read()
    return key

def encriptar_fichero(fichero):
    key = obtener_key()

    llave = Fernet(key)
    with open(fichero, "rb") as f:
        fichero_original = f.read()

    fichero_encriptado = llave.encrypt(fichero_original)
    with open(fichero, "wb") as f:
        f.write(fichero_encriptado)

def desencriptar_fichero(fichero):
    key = obtener_key()
    llave = Fernet(key)
    with open(fichero, "rb") as f:
        fichero_encriptado = f.read()

    try:
        fichero_original = llave.decrypt(fichero_encriptado)
    except Fernet.InvalidToken:
        print("Invalid token, most likely the password is incorrect")
        return

    with open(fichero, "wb") as f:
        f.write(fichero_original)

def historial(variables_historial):
    DNI = variables_historial[0]
    nombre = variables_historial[1]
    apellido = variables_historial[2]
    fecha_actual = datetime.now()
    fecha = fecha_actual.strftime('%Y-%m-%d')
    fichero=f"{DNI}_{nombre}_{apellido}_voz_{fecha}.txt"
    mode = None
    carpeta_general = "historiales"
    carpeta = f'{DNI}_{nombre}_{apellido}'

    if not os.path.exists(carpeta_general):os.mkdir(carpeta_general)
    ruta_carpeta = os.path.join(carpeta_general,carpeta)
    if not os.path.exists(ruta_carpeta):os.makedirs(ruta_carpeta)

    ruta = os.path.join(ruta_carpeta, fichero)
    if os.path.exists(ruta):
        with open(ruta, mode, encoding='utf-8') as f:
            desencriptar_fichero(ruta)
            f.write(f"\n---------------------------------------\n")

    with open(ruta, "w", encoding='utf-8') as f:       
        f.write(f"Consulta {fecha_actual.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"\nDATOS PERSONALES\n")
        f.write(f"\n-DNI: {DNI}\n")
        f.write(f"\n-Nombre: {nombre}\n")
        f.write(f"\n-Apellidos: {apellido}\n")
        f.write(f"\n-Edad: {variables_historial[3]}\n")
        f.write(f"\n-Sexo: {variables_historial[4]}\n")
        f.write(f"\n-Profesión: {variables_historial[5]}\n")
        f.write(f"\nASPECTOS RELACIONADOS CON LA SALUD EN GENERAL\n")
        f.write(f"\n-Tabaco u otras sustancias: {variables_historial[6]}\n")
        f.write(f"\n-Alcohol -consumo habitual-: {variables_historial[7]}\n")
        f.write(f"\n-Café o té -consumo habitual-: {variables_historial[8]}\n")
        f.write(f"\n-Bebidas estimulantes -consumo habitual-: {variables_historial[9]}\n")
        f.write(f"\n-Las bebidas frías dañan su voz: {variables_historial[10]}\n")
        f.write(f"\n-Reflujo gastro-esofágico: {variables_historial[11]}\n")
        f.write(f"\n-Trastornos psicoemocionales: {variables_historial[12]}\n")
        f.write(f"\n-Infecciones de repetición: {variables_historial[13]}\n")
        f.write(f"\n\nASPECTOS RELACIONADOS CON LA VOZ EN GENERAL\n")
        f.write(f"\n-Duración de los problemas de voz: {variables_historial[14]}\n")
        f.write(f"\n-Desde que comenzó el trastorno: {variables_historial[15]}\n")
        f.write(f"\n-En algún ha desaparecido totalmente: {variables_historial[16]}\n")
        f.write(f"\n-El momento del día en el que más dificultades o nota peor su voz es: {variables_historial[17]}\n")
        f.write(f"\n-La situación/situaciones en la que aparecen con más frecuencia sus molestias al hablar es: {variables_historial[18]}\n")
        f.write(f"\n-Los trastornos aparecieron: {variables_historial[19]}\n")
        f.write(f"\n-La ronquera y fatiga aumentan por: {variables_historial[20]}\n")
        
    encriptar_fichero(ruta)

def historial_VHI(DNI, nombre, apellido, variables_VHI):
    puntuacion_F = sum(variables_VHI[:10])
    puntuacion_P = sum(variables_VHI[10:20])
    puntuacion_E = sum(variables_VHI[20:30])
    fecha_actual = datetime.now()
    fecha = fecha_actual.strftime('%Y-%m-%d')
    ficheroVHI=f"{DNI}_{nombre}_{apellido}_VHI_{fecha}.txt"

    carpeta_general = "historiales"
    carpeta = f'{DNI}_{nombre}_{apellido}'

    if not os.path.exists(carpeta_general):os.mkdir(carpeta_general)
    ruta_carpeta = os.path.join(carpeta_general,carpeta)
    if not os.path.exists(ruta_carpeta):os.makedirs(ruta_carpeta)

    rutaVHI = os.path.join(ruta_carpeta, ficheroVHI)

    with open(rutaVHI, "w", encoding='utf-8') as f:  
        f.write(f"Consulta {fecha_actual.strftime('%Y-%m-%d %H:%M:%S')} \n")
        f.write("\nSe indica la frecuencia de la experiencia de la siguiente forma: : 0 = nunca, 1 = casi nunca, 2 = algunas veces, 3 = casi siempre, 4 = siempre\n")        
        f.write(f"\nParte I-F (Funcional) -{puntuacion_F} puntos-\n")
        f.write(f"\nF.1. La gente me oye con dificultad debido a mi voz: {variables_VHI[0]}.\n")
        f.write(f"\nF.2. La gente no me entiende en sitios ruidosos: {variables_VHI[1]}.\n")
        f.write(f"\nF.3. Mi familia no me oye si la llamo desde otro lado de la casa: {variables_VHI[2]}.\n")
        f.write(f"\nF.4. Uso el teléfono menos de lo que desearía: {variables_VHI[3]}.\n")
        f.write(f"\nF.5. Tiendo a evitar las tertulias debido a mi voz: {variables_VHI[4]}.\n")
        f.write(f"\nF.6. Hablo menos con mis amigos, vecinos y familiares: {variables_VHI[5]}.\n")
        f.write(f"\nF.7. La gente me pide que repita lo que les digo: {variables_VHI[6]}.\n")
        f.write(f"\nF.8. Mis problemas con la voz alteran mi vida personal y social: {variables_VHI[7]}.\n")
        f.write(f"\nF.9. Me siento desplazado de las conversaciones por mi voz: {variables_VHI[8]}.\n")
        f.write(f"\nF.10. Mi problema con la voz afecta al rendimiento laboral: {variables_VHI[9]}.\n")
        f.write(f"\n\nParte II-P (Física) -{puntuacion_P} puntos-\n")
        f.write(f"\nP.1. Me quedo sin aire al hablar: {variables_VHI[10]}.\n")
        f.write(f"\nP.2. Mi voz suena distinto a lo largo del día: {variables_VHI[11]}.\n")
        f.write(f"\nP.3. La gente me pregunta ¿Qué te pasa con la voz? {variables_VHI[12]}.\n")
        f.write(f"\nP.4. Mi voz suena cascada y seca: {variables_VHI[13]}.\n")
        f.write(f"\nP.5. Siento que necesito tensar la garganta para producir la voz: {variables_VHI[14]}.\n")
        f.write(f"\nP.6. La calidad de mi voz es impredecible: {variables_VHI[15]}.\n")
        f.write(f"\nP.7. Trato de cambiar mi voz para que suene diferente: {variables_VHI[16]}.\n")
        f.write(f"\nP.8. Hago bastante esfuerzo para hablar: {variables_VHI[17]}.\n")
        f.write(f"\nP.9. Mi voz empeora por la tarde: {variables_VHI[18]}.\n")
        f.write(f"\nP.10. Mi voz “se me acaba” a la mitad del habla: {variables_VHI[19]}.\n")
        f.write(f"\n\nParte III-E (Emocional) -{puntuacion_E} puntos-\n")
        f.write(f"\nE.1. Me siento tenso al hablar con otros debido a mi voz: {variables_VHI[20]}.\n")
        f.write(f"\nE.2. Las personas parecen irritadas por mi voz: {variables_VHI[21]}.\n")
        f.write(f"\nE.3. Creo que la gente no comprende mi problema con la voz: {variables_VHI[22]}.\n")
        f.write(f"\nE.4. Mi problema vocal me molesta: {variables_VHI[23]}.\n")
        f.write(f"\nE.5. Salgo menos por mi problema de voz: {variables_VHI[24]}.\n")
        f.write(f"\nE.6. Mi voz me hace sentir en desventaja: {variables_VHI[25]}.\n")
        f.write(f"\nE.7. Me siento contrariado  cuando me piden que repita lo dicho: {variables_VHI[26]}.\n")
        f.write(f"\nE.8. Me siento avergonzado cuando me piden que repita lo dicho: {variables_VHI[27]}.\n")
        f.write(f"\nE.9. Mi voz me hace sentir incompetente: {variables_VHI[28]}.\n")
        f.write(f"\nE.10. Me avergüenza mi problema de la voz: {variables_VHI[29]}.\n")

    encriptar_fichero(rutaVHI)

def fichero_consulta(DNI, nombre, apellido, consulta):
    fecha_actual = datetime.now()
    fecha = fecha_actual.strftime('%Y-%m-%d')
    ficheroConsulta=f"{DNI}_{nombre}_{apellido}_consulta_{fecha}.txt"

    carpeta_general = "historiales"
    carpeta = f'{DNI}_{nombre}_{apellido}'

    if not os.path.exists(carpeta_general):os.mkdir(carpeta_general)
    ruta_carpeta = os.path.join(carpeta_general,carpeta)
    if not os.path.exists(ruta_carpeta):os.makedirs(ruta_carpeta)

    rutaConsulta = os.path.join(ruta_carpeta, ficheroConsulta)

    with open(rutaConsulta, "w", encoding='utf-8') as f:
        f.write(f"{consulta}")
    
    encriptar_fichero(rutaConsulta)


def guardado_temporal(variables):
    fichero = f"guardado_temporal.txt"
    carpeta_general = "historiales"
    if not os.path.exists(carpeta_general):os.mkdir(carpeta_general)
    ruta = os.path.join(carpeta_general, fichero)

    with open(ruta, "w", encoding='utf-8') as f:  
        f.write(variables)

def obtener_temporal(variables):
    fichero = f"guardado_temporal.txt"
    carpeta_general = "historiales"
    ruta = os.path.join(carpeta_general, fichero)

    with open(ruta, "r", encoding='utf-8') as f:  
        variables = f.read()
        print(variables)

def eliminar_temporal():
    fichero = "guardado_temporal.txt"
    carpeta_general = "historiales"
    ruta = os.path.join(carpeta_general, fichero)
    if os.path.exists(ruta):os.remove(ruta)
        