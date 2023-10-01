import json
import openai
import os
import datetime
import PyPDF2 as pdf

def getDatetime():
    today = datetime.date.today()
    current_time = datetime.datetime.now().replace(microsecond=0)
    dateNow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return today, current_time, dateNow

def openJsonFile(file):
    with open(file, encoding='utf-8') as jsonFile:
        config = json.load(jsonFile)
    jsonFile.close()
    return config
        
def createJsonFile(file):
    [today, current_time, date] = getDatetime()
    if not os.path.exists(file):
        print("Archivo creado.")
        with open(file, "w", encoding='utf-8') as jsonFile:
            datos = {}
            datos.update(
                {
                    "0":{
                        "T: ": date,
                        "Q: ": "Este es un ejemplo",
                        "A: ": "Debe ser eliminado"
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
    if str(length) not in json_data:
        new_info = {
            "T": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Q": prompt,
            "A": response
        }
        json_data[str(str(length))]= new_info
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

def configureAssistant_Lector(st, texto):
    behaviour = {
        "role": "system",
        "content": f"""Eres un muy inteligente, muy útil, eficaz y eficiente asistente que tiene que leer, entender, resumir y responder preguntas 
        sobre el siguiente texto: {texto.strip()}"""
    }
    st.session_state.messages.append(behaviour)
    return st

def preguntaAbierta(st, message_placeholder, params):
    paramsOAI = params["account_type"]["enterprise"]

    full_response = ""
    for response in openai.ChatCompletion.create(
                engine=paramsOAI["OPENAI_MODEL"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
                max_tokens = params["init"]["max_tokens"],
                temperature = params["init"]["temperature"],
                top_p = params["init"]["top_p"],
                frequency_penalty = params["init"]["frequency_penalty"],
                presence_penalty = params["init"]["presence_penalty"]
            ):
        full_response += response.choices[0].delta.get("content", "")
        message_placeholder.markdown(full_response + "▌")
    message_placeholder.markdown(full_response)
    
    return full_response

def headerStreamlit(st):
    st.title("Chat with your paper")
    st.markdown("""
    <div style="padding: 7px; border: 2px solid; border-radius: 10px;">
        Engage in a dialogue with your paper using OpenAI's ChatGPT, it will respond to all your questions as accurately as possible.<br>
    </div>
    """,
    unsafe_allow_html=True
    )

def readPDFFile(filePath):
    with open(filePath, "rb") as pdfFile:
        pdfReader = pdf.PdfReader(pdfFile)
        pages = len(pdfReader.pages)
        text = ''
        for page in range(pages):
            current_page = pdfReader.pages[page]
            text += current_page.extract_text()
    return text

def getFilesInPath(path, extension):
    files = os.listdir(path.strip())
    files = [file for file in files if os.path.splitext(file)[1] == f".{extension.strip()}"]
    return files

def load_pdf(file):
    pdf_reader = pdf.PdfReader(file)
    pages = len(pdf_reader.pages)
    text = ''
    for page in range(pages):
            current_page = pdf_reader.pages[page]
            text += current_page.extract_text()
    return text