import streamlit as st
import PyPDF2 as pdf

def load_pdf(file):
    pdf_reader = pdf.PdfReader(file)
    pages = len(pdf_reader.pages)
    text = ''
    for page in range(pages):
            current_page = pdf_reader.pages[page]
            text += current_page.extract_text()
    return text

# Interfaz de usuario
st.title("Chat with your paper")

st.sidebar.title("Load your 'paper'.pdf")
file = st.sidebar.file_uploader("Load your paper into *.pdf file format", type=["pdf"])

if file is not None:
    text = load_pdf(file)
    st.write(text)