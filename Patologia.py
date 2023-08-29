import streamlit as st
import parselmouth
import matplotlib.pyplot as plt
from parselmouth.praat import call
import numpy as np
from PIL import Image
import requests
import Mensajes
import os
from datetime import datetime

#Praat
def measure2Pitch(voiceID, f0min, f0max, unit):        
    sound = parselmouth.Sound(voiceID) # read the sound
    duration = call(sound, "Get total duration") # duration
    pitch = call(sound, "To Pitch (cc)", 0, f0min, 15, 'no', 0.03, 0.45, 0.15, 0.35, 0.14, f0max)
    pulses = call([sound, pitch], "To PointProcess (cc)")
    
    # "Voice report"       
    stdevF0 = np.log(round(call(pitch, "Get standard deviation", 0 ,0, unit), 3))# get standard deviation
    harmonicity = call(sound, "To Harmonicity (cc)", 0.01, f0min, 0.1, 1.0)
    hnr = np.log(call(harmonicity, "Get mean", 0, 0))
    
    localJitter = np.log(round(100*call(pulses, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3), 3))
    localabsoluteJitter = (call(pulses, "Get jitter (local, absolute)", 0, 0, 0.0001, 0.02, 1.3))
    rapJitter = np.log(round(100*call(pulses, "Get jitter (rap)", 0, 0, 0.0001, 0.02, 1.3), 3))
    ppq5Jitter = np.log(round(100*call(pulses, "Get jitter (ppq5)", 0, 0, 0.0001, 0.02, 1.3), 3))
    ddpJitter = np.log(round(100*call(pulses, "Get jitter (ddp)", 0, 0, 0.0001, 0.02, 1.3), 3))
    localShimmer =  np.log(round(100*call([sound, pulses], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6), 3))
    localdbShimmer = np.log(round(call([sound, pulses], "Get shimmer (local_dB)", 0, 0, 0.0001, 0.02, 1.3, 1.6), 3))
    apq3Shimmer = np.log(round(100*call([sound, pulses], "Get shimmer (apq3)", 0, 0, 0.0001, 0.02, 1.3, 1.6), 3))
    aqpq5Shimmer = np.log(round(100*call([sound, pulses], "Get shimmer (apq5)", 0, 0, 0.0001, 0.02, 1.3, 1.6), 3))
    apq11Shimmer =  np.log(round(100*call([sound, pulses], "Get shimmer (apq11)", 0, 0, 0.0001, 0.02, 1.3, 1.6), 3))
    ddaShimmer = np.log(round(100*call([sound, pulses], "Get shimmer (dda)", 0, 0, 0.0001, 0.02, 1.3, 1.6), 3))
    
    row=[stdevF0, hnr, localJitter, localabsoluteJitter, rapJitter, ppq5Jitter, ddpJitter, localShimmer, localdbShimmer, apq3Shimmer, aqpq5Shimmer, apq11Shimmer, ddaShimmer]
    return row

# Grafica radar
def radar(usuario,bbdd,DNI,nombre,apellido):
    variables = ['stdevF0', ' hnr', ' localJitter', ' localabsoluteJitter', ' rapJitter', ' ppq5Jitter', ' ddpJitter', ' localShimmer', ' localdbShimmer', ' apq3Shimmer', 'aqpq5Shimmer', 'apq11Shimmer', 'ddaShimmer']
    
    # Base de datos SVD Hombres
    if bbdd=="hombres_svd":
        normal = [3.3135188817549253, 2.6905156369325334, 0.6431182496653391, 0.0001527118694049364, -0.3688121347640565, -0.14863099554710474, 0.7297715912122202, 2.09971644363273, -0.14866170084633568, 0.8398820926426991, 1.3791016380778705, 2.1228702479585393, 1.9384921290136674]
        estandar_inf = [2.7867021405781296, 2.5341371146115943, 0.4470697898809131, 0.00011625102346923019, -0.6364465969646231, -0.4019739571588405, 0.46209529361262, 1.9029900456798523, -0.3323069883195498, 0.5763609913889596, 1.1177252064170227, 1.8038915058977794, 1.6749533147509084]
        estandar_sup = [3.840335622931721, 2.8468941592534724, 0.8391667094497652, 0.0001891727153406426, -0.10117767256348986, 0.10471196606463101, 0.9974478888118206, 2.2964428415856077, 0.03498358662687845, 1.1034031938964386, 1.6404780697387182, 2.4418489900192992, 2.2020309432764265]

    # Base de datos SVD Mujeres
    elif bbdd=="mujeres_svd":
        normal = [3.736686715164471, 2.8450886876099024, 0.5390658725472444, 8.030706512930244e-05, -0.2805031638967828, -0.22798555931522757, 0.8180824663662382, 1.8699301713365692, -0.32114892892868935, 0.6855308169432306, 1.0704407991694442, 1.8239348495207983, 1.7841334707441399]
        estandar_inf = [3.40542957530055, 2.715400175924889, 0.29928271109920235, 5.532569554086357e-05, -0.5861093221475151, -0.48216130768755705, 0.5124741849432509, 1.6684708068396275, -0.5054457844063744, 0.38635489993288147, 0.8270592462704645, 1.5792615445540608, 1.484946536233038]
        estandar_sup = [4.067943855028392, 2.9747771992949157, 0.7788490339952864, 0.00010528843471774131, 0.025102994353949415, 0.02619018905710191, 1.1236907477892255, 2.0713895358335113, -0.13685207345100428, 0.9847067339535798, 1.313822352068424, 2.068608154487536, 2.0833204052552414]
   
    # Base de datos SVD General
    elif bbdd=="svd":
        normal = [3.568487513241434, 2.7836495570567523, 0.5804242306446573, 0.00010908626178144717, -0.31560389048756043, -0.1964439976913049, 0.7829809828665338, 1.9612647779905636, -0.2525893366940629, 0.746881797189707, 1.1931261799343078, 1.9427545977957363, 1.8454873853875486]
        estandar_inf = [3.1001765419132385, 2.62372469488637, 0.3512679450768744, 6.261123028413318e-05, -0.6099012517411715, -0.4532423865221059, 0.4886670335693447, 1.7321747954579663, -0.45506223997704565, 0.4515220554803339, 0.9004465750152585, 1.6298431244885219, 1.550113714054662]
        estandar_sup = [4.03679848456963, 2.9435744192271347, 0.8095805162124402, 0.00015556129327876116, -0.021306529233949434, 0.06035439113949606, 1.0772949321637229, 2.190354760523161, -0.05011643341108021, 1.0422415388990802, 1.485805784853357, 2.255666071102951, 2.1408610567204356]

    # Base de datos Thalento General
    elif bbdd=="thalento":
        normal = [3.7383734001178555, 2.6842029904205433, 0.5025744525377434, 9.932399376240888e-05, -0.5076366086370933, -0.29574728482520213, 0.5910041445998045, 2.078227123501141, -0.2205945617871432, 0.876680725524692, 1.3536811907986284, 2.1398918834964067, 1.975308720334702]
        estandar_inf = [3.422877842941769, 2.530052800060243, 0.34370424500457586, 6.562745106323116e-05, -0.6974019563785109, -0.46874121778563194, 0.40123387867065996, 1.9192785929525988, -0.3495804975468807, 0.6325005806624876, 1.1222587115142681, 1.9292089915000852, 1.7311152015038074]
        estandar_sup = [4.0538689572939415, 2.8383531807808438, 0.6614446600709109, 0.0001330205364615866, -0.31787126089567563, -0.12275335186477229, 0.7807744105289491, 2.237175654049683, -0.09160862602740574, 1.1208608703868963, 1.5851036700829886, 2.350574775492728, 2.2195022391655965]

    angulos = [i/13*2*np.pi for i in range(13)]

    estandar_sup += estandar_sup[:1]
    estandar_inf += estandar_inf[:1]
    normal += normal[:1]
    usuario += usuario[:1] 
    angulos += angulos[:1] 

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(7,5), gridspec_kw={'left': -0.1}, subplot_kw=dict(polar=True))
    plt.xticks(angulos[:-1], variables, color='grey', size=10)
    ax.plot(angulos, estandar_sup, linewidth=1, linestyle="solid", color='b')
    ax.plot(angulos, estandar_inf, linewidth=1, linestyle="solid", color='b', label="Zona estándar")
    ax.plot(angulos, usuario, marker='o', linestyle='None', color='red', label="Sus datos")
    ax.fill_between(angulos, estandar_sup, estandar_inf, alpha=0.1)
    ax.plot(angulos, normal, linewidth=1, linestyle="--", label='Media estándar')
    legend = ax.legend(loc='upper left', bbox_to_anchor=(1, 1), shadow=True, fontsize='10')

    fecha_actual = datetime.now()
    fecha = fecha_actual.strftime('%Y-%m-%d')
    grafica = f"{DNI}_{nombre}_{apellido}_radar_{fecha}.jpg"

    carpeta_general = "historiales"
    carpeta = f'{DNI}_{nombre}_{apellido}'

    if not os.path.exists(carpeta_general):os.mkdir(carpeta_general)
    ruta_carpeta = os.path.join(carpeta_general,carpeta)
    if not os.path.exists(ruta_carpeta):os.makedirs(ruta_carpeta)
    rutaRadar = os.path.join(ruta_carpeta, grafica)

    plt.savefig(rutaRadar)

    return rutaRadar

#Obtener datos de la deteccion de patologia
def detectar_patologia(url_path):
    try: 
        respuesta = requests.post(url_path, files= {"audio_data": open("audio.wav", "rb")})
        info = respuesta.text.split("(")
        info2 = info[1].split(")")
        cadenas = info2[0].split(", ")
        prob_path = float(cadenas[1])
        prob_health = float(cadenas[2])
        st.session_state["prob_path"] = prob_path
        st.session_state["prob_health"] = prob_health
        resultado = mostrar_patologia(prob_path, prob_health)
    except requests.exceptions.ConnectTimeout:
        resultado = None
    return resultado

#Mostrar datos de la deteccion de patologia
def mostrar_patologia(prob_path, prob_health):
    if prob_path>2/3 and prob_health<1/3:
        st.markdown("""
        <style>
            .patologico{
                background-color: lightcoral;
                box-shadow: 0 0 20px 5px rgba(240, 128, 128, 0.7);

            }       
        </style>
        """, unsafe_allow_html=True)
        resultado = "patologico"

    elif prob_path<1/3 and prob_health>2/3:
        st.markdown("""
        <style>
            .sano{
                background-color: lightgreen;
                box-shadow: 0 0 20px 5px rgba(144, 238, 144, 0.7);
            }       
        </style>
        """, unsafe_allow_html=True)
        resultado = "sano"

    else:
        st.markdown("""
        <style>
            .duda{
                background-color: rgb(255, 255, 113);
                box-shadow: 0 0 20px 5px rgba(255, 255, 113, 0.7);
            }       
        </style>
        """, unsafe_allow_html=True)
        resultado = "duda"
    return resultado

def parte_patologia(col1,col2,url_path,bbdd,DNI,nombre,apellido):
    # Análisis de existencia de patología
    if (st.session_state["path_seccion"] == "4"):
        st.session_state["path_seccion"] = "1"
        st.session_state["repetir_prueba"] = False

    if st.session_state["repetir_prueba"] and (st.session_state["salir"] == "no"):
        st.session_state["path_seccion"] = "4"
        Mensajes.inicio_path()

    if st.session_state["path_seccion"] == "1":
        
        #Gráfica radar
        with col1:
            sound = "audio.wav"
            datos = measure2Pitch(sound, 75, 500, "Hertz") 
            rutaRadar = radar(datos,bbdd,DNI,nombre,apellido)
            path = '<div class="texto">En la siguiente gráfica puede comparar sus resultados con los estándares, el nivel normal estaría dentro de la zona <span style="color:blue">azul</span>.</div>'
            st.markdown(path, unsafe_allow_html=True)
            image = Image.open(rutaRadar)
            st.image(image)
            st.session_state["hay_graficas"] = rutaRadar
            path_ayuda = '<div class="texto"><b>Jitter</b>: frecuencia <br><b>Shimmer</b>: amplitud<br><b>hnr</b>: ruido</div>'
            st.markdown(path_ayuda, unsafe_allow_html=True)
        
            #Obtener datos de patología
            with col2:
                with st.spinner('Detectando patología...'):
                    resultado_path = detectar_patologia(url_path)

                if resultado_path == "patologico":
                    txt = "Su resultado es patológico. Debería acudir al médico para recibir tratamiento."
                    st.session_state["repetir_prueba"] = False

                elif resultado_path == "sano":
                    txt = "Su resultado es negativo, no existe patología."
                    st.session_state["repetir_prueba"] = False
            
                elif resultado_path == "duda":
                    txt = "El resultado no es concluyente, te recomiendo ir al médico para una consulta presencial."
                    Mensajes.message(txt,False)
                    txt = "Se va a volver a realizar la prueba para ver si se llega a alguna conclusión, ¿te parece  bien? si no quieres volver a hacerla di 'salir' o pulsa el botón para terminar."
                    st.session_state["repetir_prueba"] = True
                    st.session_state["hay_graficas"] = "" #Se elimina para mostrar la de la nueva grabación
                else:
                    st.session_state["repetir_prueba"] = False
                    txt = "Lo siento, no es posible conectarse con el servicio encargado de devolver la existencia de patología."

                st.session_state["path_seccion"] = "3"  
                Mensajes.message(txt,False)             
        
        if st.session_state["repetir_prueba"] == False:
            Mensajes.message("¿Tienes alguna consulta más relacionada con la actual? Diga 'sí' o  'no'.", False)

    elif (st.session_state["sintomas_seccion"] == False) and (st.session_state["preguntas_seccion"] == "54") and st.session_state["path_seccion"] != "4":
        st.session_state["path_seccion"] = "1"