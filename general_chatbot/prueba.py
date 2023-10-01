import functions.databases as db
import os

if __name__ == "__main__":
    msg = db.creatingDB('./dbs/LLM_DB.db','llm_logs',True)
    db.testingDB('./dbs/LLM_DB.db', 'llm_logs', 'Pregunta prueba', 'respuesta prueba', 0)