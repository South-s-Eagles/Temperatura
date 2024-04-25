import mysql.connector
import datetime


def conectar_bd():
    AMBIENTE_DOCKER = True

    if AMBIENTE_DOCKER:
        HOST = "temperatura"
    else:
        HOST = "localhost"
        
    USER = "root"
    PORT = "3306"
    PASSWORD = "123456"
    DATABASE = "temperatura"

    try:
        CONEXAO = mysql.connector.connect(
             host = HOST,
             user = USER,
             port = PORT,
             password = PASSWORD,
             database = DATABASE
        )
        return CONEXAO
    except Exception as E:
        print(f"Erro ao conectar ao banco de dados: {E}")
        return None

def inserir_dados(CONEXAO, listaCaptura, bateria):
    try:
        cursor = CONEXAO.cursor()
        cursor.execute(
            """INSERT INTO temperatura (graus, data)
            VALUES
            ({}, '{}'),
            ({}, '{}');"""
            .format(listaCaptura[0]["graus"], listaCaptura[0]["data_atual"]
                    , listaCaptura[1]["graus"], listaCaptura[1]["data_atual"])
            )
        cursor.execute(
            """INSERT INTO sensor (graus, data)
            VALUE
            ({});""".format(bateria, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
        CONEXAO.commit()
        cursor.close()
        print("Dados inseridos com sucesso.")
    except Exception as e:
        print(f"Erro ao inserir dados: {e}")