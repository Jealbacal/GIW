"""
Asignatura: GIW
Práctica 4
Grupo: 04
Autores: Jesús Alberto Barrios Caballero
#           José Javier Carrasco Ferri
#           Enrique Martín Rodríguez
#           Felipe Ye Chen

Declaramos que esta solución es fruto exclusivamente de nuestro trabajo personal. No hemos
sido ayudados por ninguna otra persona o sistema automático ni hemos obtenido la solución
de fuentes externas, y tampoco hemos compartido nuestra solución con otras personas
de manera directa o indirecta. Declaramos además que no hemos realizado de manera
deshonesta ninguna otra actividad que pueda mejorar nuestros resultados ni perjudicar los
resultados de los demás.
"""
import sqlite3
import csv
from datetime import datetime

def crear_bd(db_filename):

    conn = sqlite3.connect(db_filename)
    cur = conn.cursor()

    #Creamos el fichero nos conectamos y dropeamos las tablas en caso de que existan y creamos las tablas segun lo pedido
    cur.execute("DROP TABLE IF EXISTS Datos_generales")
    cur.execute("DROP TABLE IF EXISTS IBEX35")
    cur.execute("DROP TABLE IF EXISTS SemanalesIBEX35")

    cur.execute(
        "CREATE TABLE Datos_generales (Ticker TEXT PRIMARY KEY, Nombre TEXT, Índice TEXT, País TEXT)")
    cur.execute("CREATE TABLE IBEX35 (Ticker TEXT PRIMARY KEY REFERENCES Datos_generales(Ticker),Precio REAL, Var_Porcentage REAL, Var_Euros REAL,MAX REAL,MIN REAL,Volumen REAL)")
    cur.execute(
        "CREATE TABLE SemanalesIBEX35 (Ticker TEXT REFERENCES Datos_generales(Ticker), Fecha TEXT, Price REAL)")

    conn.commit()
    conn.close()

#Funcion auxiliar para coambiar el formato a la fecha
def nueva_fecha(fecha):
    x = datetime.strptime(fecha,
                          '%d/%m/%Y %H:%M')
    fechaISO = x.strftime('%Y-%m-%d %H:%M')
    return fechaISO

def cargar_bd(db_filename, tab1, tab2, tab3):

    conn = sqlite3.connect(db_filename)
    cur = conn.cursor()
    #Recorremos cada linea del csv para meterlas en la tabla correspiente
    with open(tab1, newline='', encoding='utf-8') as file:
        r = csv.reader(file, delimiter=';')
        next(r)
        cur.executemany("INSERT INTO Datos_generales VALUES (?,?,?,?)", r)

    with open(tab2, newline='', encoding='utf-8') as file:
        r = csv.reader(file, delimiter=';')
        next(r)
        cur.executemany("INSERT INTO IBEX35 VALUES (?,?,?,?,?,?,?)", r)

    with open(tab3, newline='', encoding='utf-8') as file:
        r = csv.reader(file, delimiter=';')
        next(r)
        #se recoge la fecha y se cambia el formato
        for row in r:
            fecha = row[1]
            row[1] = nueva_fecha(fecha)
            cur.execute("INSERT INTO SemanalesIBEX35 VALUES (?,?,?)", row)
    conn.commit()
    conn.close()


def consulta1(db_filename, limite):
    
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    query = f"""
            SELECT D.Ticker,D.Nombre,I.Var_Porcentage,I.Var_Euros 
            FROM IBEX35 AS I JOIN Datos_generales AS D ON I.Ticker=D.Ticker
            WHERE Var_Porcentage >= {limite} 
            ORDER BY Var_Porcentage DESC
            """
    
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result


def consulta2(db_filename):
    
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    query = f"""
            SELECT D.Ticker,D.Nombre,MAX(I.Price)
            FROM SemanalesIBEX35 AS I JOIN Datos_generales AS D ON I.Ticker=D.Ticker
            GROUP BY D.Ticker 
            ORDER BY D.Nombre ASC
            """
    
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result



def consulta3(db_filename, limite):
   
    conn = sqlite3.connect(db_filename) 
    cursor = conn.cursor()
    #Se seleccionan una vez relacionadas las tablas,luego se busca los tickers que tienen el precio medio mayor al limite
    query = f"""
    SELECT S.Ticker, D.Nombre, AVG(S.Price) AS Media, MAX(S.Price) - MIN(S.Price) AS Diferencia
    FROM SemanalesIBEX35 AS S
    INNER JOIN Datos_generales AS D ON S.Ticker = D.Ticker 
    WHERE S.Ticker IN (
        SELECT Ticker
        FROM SemanalesIBEX35
        GROUP BY Ticker
        HAVING AVG(Price) >= {limite}
    )
    GROUP BY S.Ticker
    """
    cursor.execute(query)
    media_resultados = cursor.fetchall()
    conn.close()
    media_resultados = sorted(media_resultados, key=lambda x: x[2], reverse=True)
    return media_resultados


def consulta4(db_filename, ticker):
    conn = sqlite3.connect(db_filename) 
    cursor = conn.cursor()

    query = f'''
    SELECT Ticker, strftime('%Y-%m-%d', Fecha) as Fecha, Price
    FROM SemanalesIBEX35
    WHERE Ticker = "{ticker}"
    ORDER BY Fecha DESC
    '''
    cursor.execute(query)
    result = cursor.fetchall()
 
    conn.close()
    
    return result
    
