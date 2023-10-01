FROM python:3.11-slim-bullseye
WORKDIR /PaperReader_Chatbot

COPY . .

RUN apt-get update && \
    apt-get install -y curl && \
    apt-get install -y wget && \
    apt-get install -y gcc python3-dev && \
    apt-get -y autoremove && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip setuptools
RUN pip install -r requirements.txt

EXPOSE 1309
CMD ["streamlit", "run", "converse_with_papers.py", "--server.port=1309"]