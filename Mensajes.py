import streamlit as st
import Asistente
import Historial
import Mensajes
from os import remove

def mensaje_paciente(value):
    txt = f'<div class="paciente"> {value} </div>'
    st.markdown(txt, unsafe_allow_html=True)

def mensaje_doctor(msj):
    txt = f'<div class="doctor"> {msj} </div>'
    st.markdown(txt, unsafe_allow_html=True)

# Crea en la interfaz el mensaje escrito del doctor, con su estilo, y reproduciendolo
def message(msj,gpt):
    st.session_state["mensaje"].append([msj, "D"])
    mensaje_doctor(msj)
    Asistente.txt_audio(msj,gpt)

# Mensaje inicial
def mensaje_intro():
    txt = '<div class="doctor_inicial"> ¡Bienvenido al médico virtual!<br> Cuando pulses <i>"Iniciar consulta"</i> comenzará una grabación que va a ser usada para darte la mejor atención. Todos tus datos serán recopilados de forma segura y tratados con confidencialidad.<br>Por favor, responde a las preguntas que se te hacen, y si en algún momento quiere acabar la consulta, simplemente di <i>“Salir”</i>. </div>'
    st.markdown(txt, unsafe_allow_html=True)
    txt = '<div class="doctor_inicial"> Puede encontrar toda la información sobre el funcionamiento a la izquierda. </div>'
    st.markdown(txt, unsafe_allow_html=True)

# Mensaje de inicio de la conversación
def welcomemessage():
    mensaje_inicial = "Hola, ¿en qué puedo ayudarte? Puedes, por ejemplo, decirme tus síntomas para que te recomiende cómo calmarlos."
    message(mensaje_inicial,False)
    st.session_state["welcome"] = False

#Fin de la consulta
def goodbyemessage():
    st.session_state["sintomas_seccion"] = False
    st.session_state["salir"] = "si"
    st.session_state["path_seccion"] = "0"
    mensaje_final = "¡Hasta pronto! Ha sido un placer ayudarte."
    message(mensaje_final,False)
    remove(f'sound_gtts.wav')
    
    st.markdown("""
        <style>
            button[kind="primary"]{
                display: block;
            }     
        </style>
        """, unsafe_allow_html=True)
    
def inicio_preguntas():
    message("Antes de analizar tu voz, necesito que respondas a unas preguntas para conocer aspectos que podrían afectar a la patología. Las respuestas se van a guardar para poder ser añadidas en tu historial en caso de ser necesario.",False)
    message("Comencemos con una serie de datos personales.",False)
    st.session_state["sintomas_seccion"] = False
    st.session_state["preguntas_seccion"] = "1"
    mensajes = st.session_state["mensaje"]
    Mensajes.mensajes_anteriores(mensajes)
    Historial.guardado_temporal(st.session_state["mensajes_guardados"])
    st.experimental_rerun()

def inicio_path():
    message("Para ello debes decir la siguiente frase:",False)
    message("La casa en el campo, rodeada de árboles y flores, es el refugio perfecto para aquellos que buscan la tranquilidad y la paz.",False)
    st.session_state["sintomas_seccion"] = False

def mensajes_anteriores(mensajes):
    for x in range(len(mensajes)):
        if (mensajes[x][1] == "P"):
            st.session_state.mensajes_guardados += f'Tú: {mensajes[x][0]}\n\n'

        else:
            st.session_state.mensajes_guardados += f'Asistente: {mensajes[x][0]}\n\n'
