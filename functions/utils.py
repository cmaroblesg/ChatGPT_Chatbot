import json
import openai
import os
import datetime

def openJsonFile(file):
    with open(file, encoding='utf-8') as jsonFile:
        config = json.load(jsonFile)
    jsonFile.close()
    return config
        
def createJsonFile(file):
    if not os.path.exists(file):
        print("Archivo creado.")
        with open(file, "w", encoding='utf-8') as jsonFile:
            datos = {}
            datos.update(
                {
                    "0":{
                        "T: ":datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Q: ":"Este es un ejemplo",
                        "A: ":"Debe ser eliminado"
                    }
                }
            )
            saveJsonFile(file, datos)
        jsonFile.close()
        msg = "Archivo creado!"
    else:
        msg = "El archivo ya existe"
    return msg

def getJsonLength(json_data):
    return len(json_data)

def creatingTheLog(json_data, prompt, response):
    length = getJsonLength(json_data)
    if str(length + 1) not in json_data:
        new_info = {
            "T": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Q": prompt,
            "A": response
        }
        json_data[str(str(length + 1))]= new_info
    return json_data

def saveJsonFile(file,archivo):
    with open(file,"w", encoding='utf-8') as jsonFile:
        json.dump(archivo, jsonFile, ensure_ascii= False, indent=4)
    jsonFile.close()

def configureOpenAIEnv(config):
    openai.api_type = config['OPENAI_API_TYPE']
    openai.api_version = config['OPENAI_API_VERSION']
    openai.api_base = config['OPENAI_API_BASE']
    openai.api_key = config['OPENAI_API_KEY']
    model = config['OPENAI_MODEL']
    return openai, model

def configureStreamlit(st, model):
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = model

    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    ## Esto lo convierte en un chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    return st

def configureAssistant(st, params):
    behaviour = {
        "role": "system",
        "content": params["init"]["assistant"]
    }
    st.session_state.messages.append(behaviour)
    return st

def preguntaAbierta(st, message_placeholder):
    full_response = ""
    for response in openai.ChatCompletion.create(
                engine=st.secrets["OPENAI_MODEL"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            ):
        full_response += response.choices[0].delta.get("content", "")
        message_placeholder.markdown(full_response + "▌")
    message_placeholder.markdown(full_response)
    
    return full_response

def headerStreamlit(st):
    st.markdown("""
    <h1 style="color: #449fbd">OpenAI - ChatGPT</h1>
    <div style="background-color: #f7f7f7; padding: 7px; border: 2px solid #449fbd; border-radius: 10px;">
        Dialoga con ChatGPT de OpenAI, responderá todas tus preguntas lo más acertado posible.<br>
    </div>
    """,
    unsafe_allow_html=True
    )