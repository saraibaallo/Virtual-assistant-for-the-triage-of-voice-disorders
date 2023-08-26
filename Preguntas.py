import streamlit as st
import Traductor
import Mensajes
import Historial
import Asistente
import re

def validar_dni(dni):
    patron_dni = r'^\d{8}[a-hj-np-tv-zA-HJ-NP-TV-Z]$'
    if re.match(patron_dni, dni):return True
    else: return False

def vhi_pregunta(value, opciones,pregunta,txt,signos):
    value = value.capitalize().strip().translate(str.maketrans('', '', signos))
    puntuacion = Traductor.encontrar_similar(value, opciones)
    numero = Traductor.convertir_numero(puntuacion)
    st.session_state["respuestas_VHI"].append(numero)    
    respuesta = f"{numero}-{puntuacion}"
    st.session_state["mensaje"].append([respuesta, "P"])
    Mensajes.mensaje_paciente(respuesta)

    if st.session_state["preguntas_seccion"] == "33":
        enunciado = "Pasemos a la parte física."
        Mensajes.message(enunciado,False)
    elif st.session_state["preguntas_seccion"] == "43":
        enunciado = "Por último, la parte emocional."
        Mensajes.message(enunciado,False)
        
    st.session_state["preguntas_seccion"] = pregunta
    msj = "Respuestas posibles: nunca, casi nunca, algunas veces, casi siempre, siempre"
    Mensajes.mensaje_doctor(msj)
    Mensajes.message(txt,False)

def general_pregunta(value,pregunta,txt,msj,signos):
    valido = None
    if st.session_state["preguntas_seccion"] == "6":
        value,valido = Traductor.es_numero(value)
        st.session_state["mensaje"].append([value, "P"])

    if st.session_state["preguntas_seccion"] == "7":
        value.capitalize().strip().translate(str.maketrans('', '', signos))
        opciones = ["Masculino", "Femenino", "Otro", "Prefiero no decirlo"]
        value = Traductor.encontrar_similar(value, opciones)
        st.session_state["mensaje"].append([value, "P"])

    if st.session_state["preguntas_seccion"] == "18":
        opciones = ["Ha ido en aumento", "Permanece igual", "Intermitente"]
        value = Traductor.encontrar_similar(value, opciones)
        st.session_state["mensaje"].append([value, "P"])

    if st.session_state["preguntas_seccion"] == "20":
        opciones = ["Por la mañana", "Por la tarde", "Por la noche", "Por la mañana  y por la tarde", "Por la tarde y por la mañana", "Por la mañana  y por la noche", "Por la noche  y por la mañana", "Por la tarde  y por la noche", 
                    "Por la noche  y por la tarde", "Por la mañana, por la tarde y por la noche", "Por la mañana, por la noche y por la tarde", "Por la noche, por la tarde y por la mañana", "Por la noche, por la mañana y por la tarde", 
                    "Por la tarde, por la mañana y por la noche", "Por la tarde, por la noche y por la mañana", "Siempre"]
        value = Traductor.encontrar_similar(value, opciones)
        st.session_state["mensaje"].append([value, "P"])

    Mensajes.mensaje_paciente(value)

    if st.session_state["preguntas_seccion"] == "8":
        msg = "Perfecto, ahora vamos a pasar a aspectos relacionados con la salud en general."
        Mensajes.message(msg,False)
    
    if st.session_state["preguntas_seccion"] == "16":
        msg = "Pasemos a la última tanda de preguntas, esta vez relacionadas directamente con la voz."
        Mensajes.message(msg,False)

    if valido == False:
        msg = "Tu respuesta no es válida."
        Mensajes.message(msg,False)
        txt = f"¿Cuántos años tienes?"
        Mensajes.message(txt,False)

    else:
        st.session_state["respuestas"].append(value)
        st.session_state["preguntas_seccion"] = pregunta
        if msj == None: Mensajes.message(txt,False)
        else:
            Mensajes.mensaje_doctor(msj)
            st.session_state["mensaje"].append([txt, "D"])
            Asistente.txt_audio(txt,False)

def entrada_escrita(problema, ejemplo):
    with st.form("form"):
        st.session_state[problema] = st.text_input(f"Introduce tu {problema}: ", placeholder=f"{ejemplo}")
        msj = f"Introduce tu {problema}"
        if st.session_state["primera_vez"] == True: Asistente.txt_audio(msj, False)
        st.session_state["primera_vez"] = False

        guardado = st.form_submit_button("Guardar")
        if guardado:
            st.session_state["mensaje"].append([msj, "D"])
            if problema == "DNI":
                if validar_dni(st.session_state["DNI"]) == False:
                    st.error(f"La entrada no corresponde con un DNI válido.")
                    st.session_state["mensaje"].append([st.session_state[problema], "P"])
                    st.session_state["mensaje"].append(["La entrada no corresponde con un DNI válido.", "D"])
                    return False
                else:
                    st.session_state[problema] = st.session_state[problema].upper()
                    st.success(f"¡Guardado tu {problema} como {st.session_state[problema]}!")
                    st.session_state["mensaje"].append([st.session_state[problema], "P"])
                    return True
            else:
                st.success(f"¡Guardado tu {problema} como {st.session_state[problema]}!")
                    
        else:
            st.stop()
    
def malentendido(problema, ejemplo):
    entrada_escrita(problema, ejemplo)
    st.session_state["malentendido"] = False

def correccion(problema, ejemplo, txt, pregunta,signos):
    if st.session_state["malentendido"]:
        entrada_escrita(problema, ejemplo)
        st.session_state[problema] = st.session_state[problema].capitalize().strip().translate(str.maketrans('', '', signos))
        st.session_state["mensaje"].append([st.session_state[problema], "P"])
    st.session_state["respuestas"].append(st.session_state[problema])
    st.session_state["preguntas_seccion"] = pregunta
    if txt == None: 
        respuestas = st.session_state["respuestas"]
        txt = f"{respuestas[1]} {respuestas[2]}, ¿cuántos años tienes?"
    Mensajes.message(txt,False)

def condiciones(value, opciones,signos):
    msj = None
    if st.session_state["preguntas_seccion"] == "2":
        Mensajes.mensaje_paciente(value)
        st.session_state["nombre"] = value.capitalize().strip().translate(str.maketrans('', '', signos))
        comprobacion_nombre = "¿He entendido bien tu nombre?"
        Mensajes.message(comprobacion_nombre,False)
        st.session_state["preguntas_seccion"] = "3"
        #correccion en paciente        

    elif st.session_state["preguntas_seccion"] == "4":
        Mensajes.mensaje_paciente(value)
        st.session_state["apellido"] = value.capitalize().strip().translate(str.maketrans('', '', signos))
        comprobacion_apellido = "¿He entendido bien tu apellido?"
        Mensajes.message(comprobacion_apellido,False)
        st.session_state["preguntas_seccion"] = "5"
        #correccion en paciente 

    elif st.session_state["preguntas_seccion"] == "6":
        txt = "¿Cuál es tu sexo? Opciones: Masculino, femenino, otro, prefiero no decirlo. Esta información podría ser usada para la comparación posterior con unos u otros valores."
        general_pregunta(value,"7",txt,msj,signos)

    elif st.session_state["preguntas_seccion"] == "7":
        txt = "¿A qué te dedicas? Necesito conocer tu profesión por la implicación que la voz puede tener en ella."
        general_pregunta(value,"8",txt,msj,signos)

    elif st.session_state["preguntas_seccion"] == "8":
        txt = "¿Consumes tabaco u otras sustancias?"
        general_pregunta(value,"9",txt,msj,signos)

    elif st.session_state["preguntas_seccion"] == "9":
        txt = "¿Y alcohol, cuál dirías que es tu consumo habitual?"
        general_pregunta(value,"10",txt,msj,signos)

    elif st.session_state["preguntas_seccion"] == "10":
        txt = "¿Bebes café o té? ¿cuánto?"
        general_pregunta(value,"11",txt,msj,signos)

    elif st.session_state["preguntas_seccion"] == "11":
        txt = "¿Y bebidas estimulantes?"
        general_pregunta(value,"12",txt,msj,signos)

    elif st.session_state["preguntas_seccion"] == "12":
        txt = "¿Las bebidas frías dañan tu voz?"
        general_pregunta(value,"13",txt,msj,signos)

    elif st.session_state["preguntas_seccion"] == "13":
        txt = "¿Con cuánta frecuencia tienes reflujo gastro-esofágico? Este causa una sensación de ardor en el pecho y regurgitación de ácido estomacal."
        general_pregunta(value,"14",txt,msj,signos)

    elif st.session_state["preguntas_seccion"] == "14":
        txt = "¿Tienes algún trastorno psicoemocional, como podría ser el estrés o la depresión?"
        general_pregunta(value,"15",txt,msj,signos)

    elif st.session_state["preguntas_seccion"] == "15":
        txt = "¿Has tenido alguna infección de forma repetida?"
        general_pregunta(value,"16",txt,msj,signos)

    elif st.session_state["preguntas_seccion"] == "16":
        txt = "¿Cuánto tiempo llevas con problemas de voz?"
        general_pregunta(value,"17",txt,msj,signos)

    elif st.session_state["preguntas_seccion"] == "17":
        msj = "Dirías que desde que comenzó el trastorno:<br><ul><li> Ha ido en aumento.</li><li> Permanece igual.</li><li> Intermitente.</li></ul>"
        txt = "Dirías que desde que comenzó el trastorno, ¿ha ido en aumento, permanece igual o es intermitente?"
        general_pregunta(value,"18",txt,msj,signos)

    elif st.session_state["preguntas_seccion"] == "18":
        txt = "¿Ha desaparecido totalmente en algún momento?"
        general_pregunta(value,"19",txt,msj,signos)

    elif st.session_state["preguntas_seccion"] == "19":
        msj = "¿En qué momento del día sientes más dificultades o notas peor tu voz?<br><ul><li> Por la mañana.</li><li> Por la tarde.</li><li> Por la noche.</li></ul>"
        txt = "¿En qué momento del día sientes más dificultades o notas peor tu voz? ¿Por la mañana, por la tarde y/o por la noche?"
        general_pregunta(value,"20",txt,msj,signos)

    elif st.session_state["preguntas_seccion"] == "20":
        msj = "¿En qué situación/es aparecen con más frecuencia las molestias al hablar?<br>Algunas posibles respuestas podrían ser:<br><ul><li> En casa.</li><li> En el trabajo.</li><li> Con amigos.</li></ul>"
        txt = "¿En qué situación aparecen con más frecuencia las molestias al hablar? Algunas posibles respuestas podrían ser: en casa, en el trabajo, con amigos, ..."
        general_pregunta(value,"21",txt,msj,signos)

    elif st.session_state["preguntas_seccion"] == "21":
        msj = "¿En qué ocasión aparecieron estos trastornos?<br>Algunas posibles respuestas podrían ser:<br><ul><li> Después de una gripe.</li><li> Después de un periodo de intenso trabajo.</li><li> Tras problemas profesionales o familiares.</li><li> Después de una intervención quirúrjica.</li><li> Tras un accidente.</li></ul>"
        txt = "¿En qué ocasión aparecieron estos trastornos? Algunas posibles respuestas podrían ser: después de una gripe, después de un periodo de intenso trabajo, tras problemas profesionales o familiares, después de una intervención quirúrjica, tras un accidente, ..."
        general_pregunta(value,"22",txt,msj,signos)

    elif st.session_state["preguntas_seccion"] == "22":
        msj = "¿Qué circunstancias aumentan su ronquera y fatiga?<br>Algunas posibles respuestas podrían ser:<br><ul><li> Fumar mucho.</li><li> Ambientes ruidosos.</li><li> Dormir poco.</li><li> Hablar en público un tiempo continuado.</li></ul>"
        txt = "¿Qué circunstancias aumentan su ronquera y fatiga? Algunas posibles respuestas podrían ser: fumar mucho, ambientes ruidosos, dormir poco, hablar en público un tiempo continuado, ..."
        general_pregunta(value,"23",txt,msj,signos)
        
    elif st.session_state["preguntas_seccion"] == "23":
        st.session_state["respuestas"].append(value)
        st.session_state["preguntas_seccion"] = "24"
        Historial.historial(st.session_state["respuestas"])

        #PREGUNTAS VHI-30
        msj = "Ahora vamos a pasar a unas preguntas sobre tu percepción de la patología<br>Voy a decir una serie de afirmaciones, responde con la frecuencia con la que se cumplen <b> nunca, casi nunca, algunas veces, casi siempre, siempre</b>"
        Mensajes.mensaje_doctor(msj)
        txt = "Ahora vamos a pasar a unas preguntas sobre tu percepción de la patología. Voy a decir una serie de afirmaciones, responde con la frecuencia con la que se cumplen: nunca, casi nunca, algunas veces, casi siempre o siempre"
        st.session_state["mensaje"].append([txt, "D"])
        Asistente.txt_audio(txt,False)

        enunciado = "Empezamos con la parte funcional."
        Mensajes.message(enunciado,False)
        pregunta = "La gente me oye con dificultad debido a mi voz"
        Mensajes.message(pregunta,False)

    elif st.session_state["preguntas_seccion"] == "24":
        txt = "La gente no me entiende en sitios ruidosos."
        vhi_pregunta(value, opciones,"25",txt,signos)
    
    elif st.session_state["preguntas_seccion"] == "25":
        txt = "Mi familia no me oye si la llamo desde otro lado de la casa."
        vhi_pregunta(value, opciones,"26",txt,signos)
    
    elif st.session_state["preguntas_seccion"] == "26":
        txt = "Uso el teléfono menos de lo que desearía."
        vhi_pregunta(value, opciones,"27",txt,signos)

    elif st.session_state["preguntas_seccion"] == "27":
        txt = "Tiendo a evitar las tertulias debido a mi voz."
        vhi_pregunta(value, opciones,"28",txt,signos)

    elif st.session_state["preguntas_seccion"] == "28":
        txt = "Hablo menos con mis amigos, vecinos y familiares."
        vhi_pregunta(value, opciones,"29",txt,signos)
    
    elif st.session_state["preguntas_seccion"] == "29":
        txt = "La gente me pide que repita lo que les digo."
        vhi_pregunta(value, opciones,"30",txt,signos)

    elif st.session_state["preguntas_seccion"] == "30":
        txt = "Mis problemas con la voz alteran mi vida personal y social."
        vhi_pregunta(value, opciones,"31",txt,signos)

    elif st.session_state["preguntas_seccion"] == "31":
        txt = "Me siento desplazado de las conversaciones por mi voz."
        vhi_pregunta(value, opciones,"32",txt,signos)

    elif st.session_state["preguntas_seccion"] == "32":
        txt = "Mi problema con la voz afecta al rendimiento laboral."
        vhi_pregunta(value, opciones,"33",txt,signos)

    #Parte física                
    elif st.session_state["preguntas_seccion"] == "33":
        txt = "Me quedo sin aire al hablar."
        vhi_pregunta(value, opciones,"34",txt,signos)

    elif st.session_state["preguntas_seccion"] == "34":
        txt = "Mi voz suena distinto a lo largo del día."
        vhi_pregunta(value, opciones,"35",txt,signos)

    elif st.session_state["preguntas_seccion"] == "35":
        txt = "La gente me pregunta ¿Qué te pasa con la voz?"
        vhi_pregunta(value, opciones,"36",txt,signos)
    
    elif st.session_state["preguntas_seccion"] == "36":
        txt = "Mi voz suena cascada y seca."
        vhi_pregunta(value, opciones,"37",txt,signos)

    elif st.session_state["preguntas_seccion"] == "37":
        txt = "Siento que necesito tensar la garganta para producir la voz."
        vhi_pregunta(value, opciones,"38",txt,signos)

    elif st.session_state["preguntas_seccion"] == "38":
        txt = "La calidad de mi voz es impredecible."
        vhi_pregunta(value, opciones,"39",txt,signos)

    elif st.session_state["preguntas_seccion"] == "39":
        txt = "Trato de cambiar mi voz para que suene diferente."
        vhi_pregunta(value, opciones,"40",txt,signos)

    elif st.session_state["preguntas_seccion"] == "40":
        txt = "Hago bastante esfuerzo para hablar."
        vhi_pregunta(value, opciones,"41",txt,signos)

    elif st.session_state["preguntas_seccion"] == "41":
        txt = "Mi voz empeora por la tarde."
        vhi_pregunta(value, opciones,"42",txt,signos)

    elif st.session_state["preguntas_seccion"] == "42":
        txt = "Mi voz “se me acaba” a la mitad del habla"
        vhi_pregunta(value, opciones,"43",txt,signos)
    
    #Parte emocional
    elif st.session_state["preguntas_seccion"] == "43":
        txt = "Me siento tenso al hablar con otros debido a mi voz."
        vhi_pregunta(value, opciones,"44",txt,signos)

    elif st.session_state["preguntas_seccion"] == "44":
        txt = "Las personas parecen irritadas por mi voz."
        vhi_pregunta(value, opciones,"45",txt,signos)
    
    elif st.session_state["preguntas_seccion"] == "45":
        txt = "Creo que la gente no comprende mi problema con la voz."
        vhi_pregunta(value, opciones,"46",txt,signos)

    elif st.session_state["preguntas_seccion"] == "46":
        txt = "Mi problema vocal me molesta."
        vhi_pregunta(value, opciones,"47",txt,signos)

    elif st.session_state["preguntas_seccion"] == "47":
        txt = "Salgo menos por mi problema de voz."
        vhi_pregunta(value, opciones,"48",txt,signos)

    elif st.session_state["preguntas_seccion"] == "48":
        txt = "Mi voz me hace sentir en desventaja."
        vhi_pregunta(value, opciones,"49",txt,signos)

    elif st.session_state["preguntas_seccion"] == "49":
        txt = "Me siento contrariado cuando me piden que repita lo dicho."
        vhi_pregunta(value, opciones,"50",txt,signos)

    elif st.session_state["preguntas_seccion"] == "50":
        txt = "Me siento avergonzado cuando me piden que repita lo dicho."
        vhi_pregunta(value, opciones,"51",txt,signos)

    elif st.session_state["preguntas_seccion"] == "51":
        txt = "Mi voz me hace sentir incompetente."
        vhi_pregunta(value, opciones,"52",txt,signos)

    elif st.session_state["preguntas_seccion"] == "52":
        txt = "Me avergüenza mi problema de la voz."
        vhi_pregunta(value, opciones,"53",txt,signos)

    elif st.session_state["preguntas_seccion"] == "53":
        puntuacion = Traductor.encontrar_similar(value, opciones)
        numero = Traductor.convertir_numero(puntuacion)
        st.session_state["respuestas_VHI"].append(numero)                                      
        respuestas_historial = st.session_state["respuestas"]
        DNI = respuestas_historial[0]
        nombre = respuestas_historial[1]
        apellido = respuestas_historial[2]
        Historial.historial_VHI(DNI, nombre, apellido, st.session_state["respuestas_VHI"])
        st.session_state["preguntas_seccion"] = "54"
        txt = "¡Gracias! He guardado las respuestas para que las pueda consultar el médico."
        Mensajes.message(txt,False)
        Mensajes.message("Ahora vamos a detectar la existencia de una posible patología...",False)
        Mensajes.inicio_path()