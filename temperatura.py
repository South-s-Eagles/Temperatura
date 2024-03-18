import mysql.connector
import datetime
import random
import time
import matplotlib.pyplot as plt

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

def gerar_grafico(listaCaptura):
    tempos = []
    temperaturas = []

    for dados in listaCaptura:
        tempos.append(dados["data_atual"])
        temperaturas.append(dados["graus"])
    plt.plot(tempos, temperaturas)
    plt.xlabel('Tempo')
    plt.ylabel('Temperatura (°C)')
    plt.title('Variação da temperatura ao longo do tempo')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def capturar_dados(AMBIENTE_DOCKER):
    CONEXAO = conectar_bd(AMBIENTE_DOCKER)
    quantidade_iteracoes = 0
    listaCaptura = []
    ATRASO = 60*2 # Intervalo de captura de dados (em segundos)

    if CONEXAO:
        while True:
            if(quantidade_iteracoes < 2):
                listaCaptura.append ({
                    "graus": random.uniform(15, 35),
                    "data_atual": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                quantidade_iteracoes += 1
            else:
                inserir_dados(CONEXAO, listaCaptura)
                gerar_grafico(listaCaptura)
                listaCaptura.clear()
                quantidade_iteracoes = 0

            time.sleep(ATRASO)
            
AMBIENTE_DOCKER = True
capturar_dados(AMBIENTE_DOCKER)