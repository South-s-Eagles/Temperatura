import mysql.connector

def conectar_bd(AMBIENTE_DOCKER):
    if AMBIENTE_DOCKER:
        HOST = "mysql",
        USER = "root",
        PORT = "3306",
        PASSWORD = "123456",
        DATABASE = "temperatura"
    else:
        HOST = "localhost",
        USER = "root",
        PORT = "3306",
        PASSWORD = "123456",
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

def inserir_dados(CONEXAO, listaCaptura):
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
        CONEXAO.commit()
        cursor.close()
        print("Dados inseridos com sucesso.")
    except Exception as e:
        print(f"Erro ao inserir dados: {e}")