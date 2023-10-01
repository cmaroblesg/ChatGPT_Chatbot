import functions.utils as functions
import streamlit as st
import datetime

params = functions.openJsonFile("configuracion.json")
[today, current_time, date] = functions.getDatetime()
msg = functions.createJsonFile(f'{params["route"]["logs"]}/{today}.json')
if __name__=="__main__":
    data = functions.openJsonFile(f'{params["route"]["logs"]}/{today}.json')
    [openai, model] = functions.configureOpenAIEnv(params["account_type"]["enterprise"])
    
    # files = functions.getFilesInPath(params["route"]["data"], "pdf")
    # text = functions.readPDFFile(f'{params["route"]["data"]}/{files[0]}')

    functions.headerStreamlit(st)
    st.sidebar.title("Load your 'paper'.pdf")
    file = st.sidebar.file_uploader("Load your paper into *.pdf file format", type=["pdf"])

    if file is not None:
        text = functions.load_pdf(file)
    st = functions.configureStreamlit(st, model)

    current_time = datetime.datetime.now().replace(microsecond=0)
    if prompt := st.chat_input("¿Como te puedo ayudar hoy?"):
        st = functions.configureAssistant_Lector(st, text)
        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = functions.preguntaAbierta(st, message_placeholder, params)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

        data = functions.creatingTheLog(data, prompt, full_response)
        functions.saveJsonFile(f'{params["route"]["logs"]}/{today}.json', data)