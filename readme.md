# Description (English)
_This program is only available in Spanish._

### Patient’s access
In the patient's section you can have a conversation with the assistant in an oral way (using microphone and speaker) as well as written (the conversation is going to be showed as messages in the screen, also the patient could write some of them).

The conversation is divided in three parts:
- **Patient consultation**. Patient tells his/her symptoms and the assitant recommend him/her some treatment.
- **Medical history**. Assistant asks two questionnaires (VHI-30 and another one). Patient's answers will be save so that the doctor can read them in a future.
- **Pathology**. To detect the existence of a voice disorder.

### Doctor’s access
It is a private area, you need credentials to access to it (check "Usage" section). In this area the doctor can check the history of all his/her patients.
The doctor can read, for any patient:
- A summary, that can be reproduced, of the last answers to the questionnaires and the last symptoms communicated.
- Complete transcription of conversations.
- All the questionnaires answered.
- All the symptoms communicated.

# Descripción (Español)

### Acceso a pacientes

La parte del paciente consiste en una conversación entre este y el asistente, tanto oral (mediante
el micrófono y el altavoz) como escrita (mostrando por pantalla las respuestas y con entradas de
texto puntuales por parte del paciente).
![image](https://github.com/saraibaallo/Virtual-assistant-for-the-triage-of-voice-disorders/assets/115147932/8f1cf9e0-363f-426e-b278-3ebaf553803e)

La conversación se divide en tres partes:

- **Consulta**. El paciente comunica los síntomas y el asistente le ofrece recomendaciones para tratarlos.
- **Historial**. El asistente lleva a cabo dos cuestionatios (VHI-30 y otro adicional). Las respuestas del paciente se guardan para que el médico pueda consultarlas cuando atienda al paciente.
- **Patología**. Se detecta la posible existencia de patolgía en la voz.

### Acceso a médicos
Es un acceso privado en el que los médicos, con su identificación (para la creación de identificación válida ver apartado "uso"), pueden acceder al historial de sus pacientes. Concretamente de cada uno de ellos ven:
- Un resumen (escrito y con opción de reproducible) de las respuestas de la última vez que hizo los cuestionarios y sus síntomas comunicados.
- Las transcripciones completas de todas las conversaciones que ha tenido con el asistente.
- Los cuestionarios que ha respondido.
- Los síntomas que ha comunicado.
![image](https://github.com/saraibaallo/Virtual-assistant-for-the-triage-of-voice-disorders/assets/115147932/62f67da1-8e98-4fa1-9c55-af8b45f06310)




# Installation (English)
Make sure that all the required libraries are installed by executing the following command:
```
pip install -r requirements.txt
```

Important. At some moments this program uses ChatGPT, you need to have a valid key given by openAI saved as _“OPENAI_API_KEY”_ in _“Environments variables”_ of your computer.
1.	Environment variables
2.	System properties
3.	System variables
4.	New…
  4.1.	As name “OPENAI_API_KEY”
  4.2.	As value the one given by OpenAI
5.	Click “Accept”

# Instalación (Español)
Asegúrate de que las librerías requeridas están instaladas, para ello:
```
pip install -r requirements.txt
```
Importante. En algunos momentos el programa usa ChatGPT, por lo que necesitas tener una clave válida dada por OpenAI guardada como “OPENAI_API_KEY” en las “variables del entorno” de tu ordenador._
1.	Ve a Variables del entorno.
2.	Abajo hay un botón de “Propiedades del sistema”, clique.
3.	Ahí verás un apartado llamado “Variables del sistema”.
4.	Clique en “Nueva…”.
  4.1.	Ponga como nombre “OPENAI_API_KEY”.
  4.2.  Ponga como valor la clave dada por OpenAI.
6.	Dé a aceptar.




# Usage (Uso)
### Patients' access (Acceso a pacientes)
For running the Patient’s section _(Para lanzar la parte del paciente)_:
```
python -m streamlit run Paciente_AsistenteTriajeVoz.py
```

El uso es guiado durante toda la consulta, pero además, hay instrucciones generales fijas en el desplegable de la izquierda.

<img width="543" alt="image" src="https://github.com/saraibaallo/Virtual-assistant-for-the-triage-of-voice-disorders/assets/115147932/2c84a7c4-da39-46cf-8e68-008a40a3cb1c">

### Doctor's access (Acceso a médicos)
For running the Doctor’s section _(Para lanzar la parte del médico)_:
```
python -m streamlit run Medico_AsistenteTriajeVoz.py
```

Ensure that your credentials are stored in "config.yaml". Go to "usernames" in "credentials" and complete your information as follows:

```
credentials:
  usernames:
    <your username>:
      email: <your email>
      name: <your name>
      password: <your codificated password>
```
