import functions.utils as functions
import streamlit as st
import logging
import datetime

date = datetime.date.today()
msg = functions.createJsonFile(f"./data/{date}.json")
if __name__=="__main__":
    data = functions.openJsonFile(f"./data/{date}.json")
    #logging.basicConfig(filename='./data/log_conversacion.log', level=logging.DEBUG)
    logging.basicConfig(filename=f'./data/log_conversacion_{date}.log', format='%(message)s', level=logging.INFO)
    #logging.basicConfig(level=logging.INFO, filename=f'./data/log_conversacion_{date}.txt', format='%(asctime)s - %(levelname)s - %(message)s')

    params = functions.openJsonFile("configuracion.json")
    [openai, model] = functions.configureOpenAIEnv(params["account_type"]["enterprise"])

    functions.headerStreamlit(st)
    st = functions.configureStreamlit(st, model)

    current_time = datetime.datetime.now().replace(microsecond=0)
    if prompt := st.chat_input("¿Como te puedo ayudar hoy?"):
        st = functions.configureAssistant(st, params)
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
            full_response = functions.preguntaAbierta(st, message_placeholder)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        #print(f'{str(current_time)};Q: {prompt};A: {full_response}')
        #logging.debug(f"Pregunta: {prompt}\nRespuesta: {full_response}")
        logging.info(f'{str(current_time)}; Q: {prompt}; A: {full_response}')
        
        data = functions.creatingTheLog(data, prompt, full_response)
        functions.saveJsonFile(f"./data/{date}.json", data)