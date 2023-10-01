import os
import re
import sqlite3 as sql
import functions.utils as ut

def creatingDB(filePath, logname, erease):
    if os.path.exists(filePath):
        msg = "The database already exists!"
    else:
        msg = f"Creating the table {filePath} and the table {logname}"
        conn = sql.connect(filePath)
        conn.execute(f'''
                        CREATE TABLE {logname}(
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            PREGUNTA TEXT,
                            RESPUESTA TEXT,
                            RATING INTEGER,
                            FECHA TEXT,
                            FECHA_SYSTEM DATE DEFAULT (DATETIME('now'))
                        );
                     ''');
        conn.commit()
        conn.close()
    return msg

def testingDB(filePath, logname, pregunta, respuesta, rating):
    [today, current_time, date] = ut.getDatetime()
    pregunta = re.sub("'",'"', pregunta)
    respuesta = re.sub("'",'"', respuesta)
    conn = sql.connect(filePath)
    conn.execute(f'''
                    INSERT INTO {logname} (pregunta, respuesta, rating, fecha)
                    VALUES ('{pregunta}', '{respuesta}', {rating}, '{date}');
                 ''')
    conn.commit()

def updatingDB(filePath, logname, pregunta, respuesta, rating):
    [today, current_time, date] = ut.getDatetime()
    pregunta = re.sub("'",'"', pregunta)
    respuesta = re.sub("'",'"', respuesta)
    conn = sql.connect(filePath)
    conn.execute(f'''
                    INSERT INTO {logname} (pregunta, respuesta, rating, fecha)
                    VALUES ('{pregunta}', '{respuesta}', {rating}, '{date}');
                 ''')
    conn.commit()
