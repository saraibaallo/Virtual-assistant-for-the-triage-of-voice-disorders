import requests
import streamlit as st
import string
import pyautogui
from PIL import Image
from audio_recorder_streamlit import audio_recorder
from screeninfo import get_monitors 
from requests.exceptions import ConnectionError, ConnectTimeout

#propios
import Historial
import Mensajes
import Asistente
import Preguntas
import Patologia

st.set_page_config(page_title="Asistente voz | Área pacientes", page_icon="favicon.png", layout="wide", initial_sidebar_state="expanded", menu_items=None)

if 'mensaje' not in st.session_state:
    st.session_state["mensaje"] = []

if 'mensajes_guardados' not in st.session_state:
    st.session_state["mensajes_guardados"] = ""

#Cargo el fichero de estilos css
with open('styles_pacientes.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def autoscroll():
    js = f"""
    <script>
        function scroll(dummy_var_to_force_repeat_execution){{
            var textAreas = parent.document.querySelectorAll('.stTextArea textarea');
            for (let index = 0; index < textAreas.length; index++) {{
                textAreas[index].scrollTop = textAreas[index].scrollHeight;
            }}
        }}
        scroll({len(st.session_state.mensajes_guardados)})
    </script>
    """

    st.components.v1.html(js)

def salir():
    with col2:
        Historial.eliminar_temporal()
        Mensajes.goodbyemessage()
        mensajes = st.session_state["mensaje"]
        Mensajes.mensajes_anteriores(mensajes)
        st.session_state["path_seccion"] = "0"
        if len(st.session_state["mensajes_guardados"]) > 178: #El paciente ha dicho algo
            with st.spinner('Por favor, espere, se está guardando la consulta...'):
                consulta = st.session_state["mensajes_guardados"]
                DNI = st.session_state["DNI"]
                nombre = st.session_state["nombre"]
                apellido = st.session_state["apellido"]
                Historial.fichero_consulta(DNI, nombre, apellido, consulta)

url = 'http://signal4.cps.unizar.es:8000/transcribe'
url_path = 'http://gtc3pc17.cps.unizar.es:5000/voicedisorder'
archivo_audio = 'audio.wav'

parametros = {
    'language': 'spanish',
    'model_size': 'medium'
}

# Establecer los headers de la llamada POST
headers = {
    'Content-Type': 'audio/mp3'
}

titulo = '<div class="intro"> Asistente virtual para el triaje de patologías de la voz </div>'
st.markdown(titulo, unsafe_allow_html=True)

footer= '<div class="footer">Creado con <i>Streamit</i> por Sara Ibáñez Alloza <br> <b>TFG 2023</b></div>'
st.markdown(footer,unsafe_allow_html=True)

with st.sidebar:
    st.title('Funcionamiento')
    st.markdown('''
    - Pulse **Iniciar consulta** para comenzar.
    - Mantenga la conversación mientras lo desee (consultar *Controles*)
    - Pulse **Acabar consulta** para finalizar o diga 'salir'.
    - Pulse **Nueva consulta** para comenzar de nuevo.    
    ''', unsafe_allow_html=False)

    st.title('Controles')
    st.markdown('''
    - Pulse 🎙️ para iniciar la grabación, cuando se esté grabando el icono cambiará a **:blue[azul]**.
    - Vuelva a pulsar 🎙️ para detenerla, el icono pasará a color **negro**.      
    ''')

# MEMORIA
if 'estado_boton' not in st.session_state:
    st.session_state["estado_boton"] = "Iniciar consulta"

if 'tamaño_micro' not in st.session_state:
    for pantalla in get_monitors():
        altura = pantalla.height_mm
        anchura = pantalla.width_mm
        
        if anchura<320: st.session_state["tamaño_micro"] = "3x"
        elif anchura<520: st.session_state["tamaño_micro"] = "5x"
        else: st.session_state["tamaño_micro"] = "7x"

if 'welcome' not in st.session_state:
    st.session_state["welcome"] = True

if 'path_seccion' not in st.session_state:
    st.session_state["path_seccion"] = "0"

if 'preguntas_seccion' not in st.session_state: 
    st.session_state["preguntas_seccion"] = "0"

if 'nombre' not in st.session_state: 
    st.session_state["nombre"] = "Anónimo"

if 'apellido' not in st.session_state: 
    st.session_state["apellido"] = ""

if 'DNI' not in st.session_state:
    st.session_state["DNI"] = "0"

if 'primera_vez' not in st.session_state: 
    st.session_state["primera_vez"] = True

if 'malentendido' not in st.session_state:
    st.session_state["malentendido"] = False

if 'respuestas' not in st.session_state:
    st.session_state["respuestas"] = []

if 'respuestas_VHI' not in st.session_state:
    st.session_state["respuestas_VHI"] = []

if 'sintomas_seccion' not in st.session_state:
    st.session_state["sintomas_seccion"] = True

if 'mas_consultas' not in st.session_state:
    st.session_state["mas_consultas"] = False

if 'salir' not in st.session_state:
    st.session_state["salir"] = "no"

if 'audio_bytes' not in st.session_state:
    st.session_state.audio_bytes = None

if 'hay_graficas' not in st.session_state:
    st.session_state["hay_graficas"] = False

if 'prob_path' not in st.session_state:
    st.session_state["prob_path"] = None

if 'prob_health' not in st.session_state:
    st.session_state["prob_health"] = None

if 'repetir_prueba' not in st.session_state:
    st.session_state["repetir_prueba"] = False

if 'opciones' not in st.session_state:
    st.session_state["opciones"] = ['Nunca', 'Casi nunca', 'Algunas veces', 'Casi siempre', 'Siempre']

if 'puntuacion' not in st.session_state:
    st.session_state["puntuacion"] = string.punctuation + "¡¿"

sample_rate = 16000
tts_language='es'
total_tokens = 0

Mensajes.mensaje_intro()

# Comienzo del programa
estado_boton = st.session_state["estado_boton"]
if st.button(estado_boton,key="empezar", type="primary"):
    st.session_state["estado_boton"] = "Nueva consulta"
    if st.session_state["salir"] == "si":
        pyautogui.hotkey('f5')

if st.session_state["estado_boton"] == "Nueva consulta" and st.session_state["salir"] == "no":
    st.markdown("""
        <style>
            button[kind="primary"]{
                display: none;
            }
            .doctor_inicial {
                display: none;
            }            
        </style>
        """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([5,10,3], gap="medium")
    with col1:
        path = '<div class="seccion">Resultados patología</div>'
        st.markdown(path, unsafe_allow_html=True)
        semaforo = '<div class="semaforo"> <div class="sano"></div><div class="duda"></div><div class="patologico"></div></div>'
        semaforo_txt = """<div class="texto_semaforo">Este semáforo indica su relación con la patología de voz.<br><br>
                        <span class="texto_sombra", style="color: lightgreen">Verde</span>: No se ha detectado patología<br>
                        <span class="texto_sombra", style="color: yellow">Amarillo</span>: Resultado no concluyente<br>
                        <span class="texto_sombra", style="color: lightcoral">Rojo</span>: Patológico
                        </div>"""
        semaforo_div = f'<div class="div_semaforo">{semaforo}{semaforo_txt}</div>'
        st.markdown(semaforo_div, unsafe_allow_html=True)
                        
        if st.session_state["hay_graficas"]:
            if st.session_state["prob_path"] != None:
                Patologia.mostrar_patologia(st.session_state["prob_path"], st.session_state["prob_health"])
            path = '<div class="texto">En la siguiente gráfica puede comparar sus resultados con los estándares, el nivel normal estaría dentro de la zona <span style="color:blue">azul</span>.</div>'
            st.markdown(path, unsafe_allow_html=True)
            image = Image.open('Gráfica_radar.jpg')
            st.image(image)
            path = '<div class="texto">**Jitter**: frecuencia <br>**Shimmer**: amplitud<br>**hnr**: ruido</div>'
            st.markdown(path, unsafe_allow_html=True)
        
    with col3:
        control = '<div class="seccion">Controles</div>'
        st.markdown(control, unsafe_allow_html=True)

    with col2:
        consulta = '<div class="seccion">Tu consulta</div>'
        st.markdown(consulta, unsafe_allow_html=True)

        if st.session_state["welcome"] == True:
            Mensajes.welcomemessage()

    with col3:
        icono = st.session_state["tamaño_micro"]
        audio_bytes = audio_recorder(text="Pulse para hablar", recording_color ="91b2eb",energy_threshold=(1,1),pause_threshold=2.0,icon_size=icono,sample_rate=sample_rate, key='audio_recorder')
        control = """<div class="control"><i>Espere un par de segundos para hablar</i><br><br>
        <b>¿Quieres salir?</b><br>Di "salir" o pulsa el botón</div>"""
        st.markdown(control, unsafe_allow_html=True)
        if st.button("Acabar consulta",key="acabar", type="secondary"):
            salir()
            

    #Las correcciones escritas tienen que estar fuera para que funcione
    with col2:
        if st.session_state["preguntas_seccion"] == "1":
            Historial.obtener_temporal(st.session_state["mensajes_guardados"])
            if Preguntas.entrada_escrita("DNI","12345678A"):
                st.session_state["respuestas"].append(st.session_state["DNI"])
                st.session_state["primera_vez"] = True
                st.session_state["preguntas_seccion"] = "2"
                txt = "¿Cuál es tu nombre?"
                Mensajes.message(txt,False)
                mensajes = st.session_state["mensaje"]
                Mensajes.mensajes_anteriores(mensajes)
                st.text_area("Consulta completa" ,height=300, key='mensajes_guardados', disabled=True)
                autoscroll()

        elif st.session_state["preguntas_seccion"] == "3.1":
            Historial.obtener_temporal(st.session_state["mensajes_guardados"])
            Preguntas.correccion("nombre", "María", "¿Y tu apellido?", "4", st.session_state["puntuacion"])
            mensajes = st.session_state["mensaje"]
            Mensajes.mensajes_anteriores(mensajes)
            st.text_area("Consulta completa" ,height=300, key='mensajes_guardados', disabled=True)
            autoscroll()
            st.session_state["primera_vez"] = True
        
        elif st.session_state["preguntas_seccion"] == "5.1":
            Historial.obtener_temporal(st.session_state["mensajes_guardados"])
            Preguntas.correccion("apellido", "Pérez", None, "6", st.session_state["puntuacion"])
            mensajes = st.session_state["mensaje"]
            Mensajes.mensajes_anteriores(mensajes)
            st.text_area("Consulta completa" ,height=300, key='mensajes_guardados', disabled=True)
            autoscroll()
            Historial.eliminar_temporal()

    # Save audio to WAV file
    if audio_bytes and audio_bytes != st.session_state.audio_bytes:
        st.session_state.audio_bytes = audio_bytes
        with open('audio.wav', mode='bw') as f:
            f.write(audio_bytes)
        files = {'audio_data': open(archivo_audio, 'rb')}

        with col2:
            try:
                respuesta = requests.post(url, files=files, data=parametros)
                print(respuesta)

            # Transcribe audio using Whisper
                if  len(respuesta.text)>0:
                    st.session_state["mensaje"] = []
                    value = respuesta.text.strip()
                    if st.session_state["preguntas_seccion"] not in ("6","7","18","20") and (int(st.session_state["preguntas_seccion"])<24 and int(st.session_state["preguntas_seccion"])<54):
                        st.session_state["mensaje"].append([value, "P"])
                    if st.session_state["preguntas_seccion"] == "0" or st.session_state["preguntas_seccion"] == "54":
                        Mensajes.mensaje_paciente(value)
                    if value.lower().strip().translate(str.maketrans('', '', st.session_state["puntuacion"])) == ("salir"):
                        salir()

                if  len(respuesta.text)>0 and st.session_state["salir"] == "no":
                    if (value.lower().strip().translate(str.maketrans('', '', st.session_state["puntuacion"])) == ("si") or value.lower().strip().translate(str.maketrans('', '', st.session_state["puntuacion"])) == ("sí")) and st.session_state["path_seccion"] == "3" and st.session_state["repetir_prueba"] == False:
                        st.session_state["path_seccion"] = "2"
                        st.session_state["mas_consultas"] = True

                    elif value.lower().strip().translate(str.maketrans('', '', st.session_state["puntuacion"])) == ("no") and st.session_state["path_seccion"] == "3" and st.session_state["repetir_prueba"] == False:
                        salir()
                    
                    elif st.session_state["path_seccion"] == "3" and st.session_state["repetir_prueba"] == False:   #Se ha respondido algo que no es ni "si" ni "no"
                        Mensajes.message("Perdona, creo que no te he entendido, di 'sí' si quieres continuar la consulta o 'no' si quieres terminar.",False)
                    
                    if (value.lower().strip().translate(str.maketrans('', '', st.session_state["puntuacion"])) == ("si") or value.lower().strip().translate(str.maketrans('', '', st.session_state["puntuacion"])) == ("sí")) and st.session_state["sintomas_seccion"] == True:
                        Mensajes.inicio_preguntas()

                    if st.session_state["preguntas_seccion"] == "3":
                        Mensajes.mensaje_paciente(value)
                        if value.lower().strip().translate(str.maketrans('', '', st.session_state["puntuacion"])) == ("no"):
                            st.session_state["malentendido"] = True
                        st.session_state["preguntas_seccion"] = "3.1"
                        mensajes = st.session_state["mensaje"]
                        Mensajes.mensajes_anteriores(mensajes)
                        Historial.guardado_temporal(st.session_state["mensajes_guardados"])
                        st.experimental_rerun()


                    elif st.session_state["preguntas_seccion"] == "5":
                        Mensajes.mensaje_paciente(value)
                        if value.lower().strip().translate(str.maketrans('', '', st.session_state["puntuacion"])) == ("no"):
                            st.session_state["malentendido"] = True
                        st.session_state["preguntas_seccion"] = "5.1"
                        mensajes = st.session_state["mensaje"]
                        Mensajes.mensajes_anteriores(mensajes)
                        Historial.guardado_temporal(st.session_state["mensajes_guardados"])
                        st.experimental_rerun()

                    # Nueva consulta
                    elif st.session_state["mas_consultas"]:
                        txt = "Genial, ¿qué más quieres saber?"
                        Mensajes.message(txt,False)
                        st.session_state["sintomas_seccion"] = True
                        st.session_state["mas_consultas"] = False

                    # Consulta a ChatGPT
                    elif st.session_state["sintomas_seccion"]:
                        respuesta_gpt = Asistente.ask_chatgpt(value)
                        Mensajes.message(respuesta_gpt,True)
                        if st.session_state["path_seccion"] != "2":
                            txt = "¿Tienes alguna duda más? Si es así, dímela para poder ayudarte. Si no, ¿quieres pasar a detectar patología? Di 'sí' para continuar."
                            Mensajes.message(txt,False)
                    
                    #PARTE DE HISTORIAL
                    opciones = st.session_state["opciones"]
                    Preguntas.condiciones(value, opciones,st.session_state["puntuacion"])
                    
                    #PARTE DE PATOLOGÍA
                    Patologia.parte_patologia(col1,col2,url_path,"svd",st.session_state["DNI"],st.session_state["nombre"],st.session_state["apellido"])

                elif len(respuesta.text)==0 and st.session_state["salir"] == "no":
                    Mensajes.message("Perdona, no te he entendido, ¿podrías repetírmelo?",False)
            
            except (ConnectTimeout, ConnectionError):
                txt = "Disculpa, está habiendo problemas para conectarse al programa que transcribe tus grabaciones. Inténtelo de nuevo, si ves que el problema persiste, comprueba la conexión a internet y pruebe más adelante."
                Mensajes.message(txt,False)

            mensajes = st.session_state["mensaje"]
            Mensajes.mensajes_anteriores(mensajes)
            st.text_area("Consulta completa" ,height=300, key='mensajes_guardados', disabled=True)
            autoscroll()