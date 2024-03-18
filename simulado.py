import mysql.connector
import random
import matplotlib.pyplot as plt

def conectar_bd(AMBIENTE_DOCKER):
    if AMBIENTE_DOCKER:
        HOST = "mysql"
        USER = "root"
        PORT = "3306"
        PASSWORD = "123456"
        DATABASE = "temperatura"
    else:
        HOST = "localhost"
        USER = "root"
        PORT = "3306"
        PASSWORD = "123456"
        DATABASE = "temperatura"

    try:
        CONEXAO = mysql.connector.connect(
             host=HOST,
             user=USER,
             port=PORT,
             password=PASSWORD,
             database=DATABASE
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
            .format(listaCaptura[-2]["graus"], listaCaptura[-2]["data_atual"]
                    , listaCaptura[-1]["graus"], listaCaptura[-1]["data_atual"])
            )
        CONEXAO.commit()
        cursor.close()
    except Exception as e:
        print(f"Erro ao inserir dados: {e}")

def dados_simulados(graus, hora, minuto):
    if (hora == 14 and minuto == 0) or (hora == 16 and minuto == 0) or (hora == 18 and minuto == 0):
        graus += random.uniform(1.1, 1.7)
    else:
        if hora < 8 and graus > 36.2:
            graus -= random.uniform(0.1, 0.7)
        elif hora >= 8 and hora < 14 and graus > 36.9:
            graus -= random.uniform(0.1, 0.7)
        elif hora >= 14 and hora < 18 and graus > 37.2:
            graus -= random.uniform(0.1, 0.7)
        elif hora >= 18 and graus > 36.5:
            graus -= random.uniform(0.1, 0.7)
        else:
            graus += random.uniform(0.1, 0.7)

    if minuto >= 58:
        hora += 1
        minuto = 0
    else:
        minuto += 2

    return graus, hora, minuto

def gerar_grafico(temperaturas, horas):
    plt.scatter(horas, temperaturas, marker='o')
    plt.xlabel('Tempo (horas)')
    plt.ylim(35.2, 39.5)
    plt.ylabel('Temperatura (°C)')
    plt.title('Variação da temperatura ao longo do tempo')
    plt.grid(True)
    plt.show()

def capturar_dados(AMBIENTE_DOCKER):
    CONEXAO = conectar_bd(AMBIENTE_DOCKER)
    dados = random.uniform(35.97, 36.5), 0, 0, 0
    quantidade_iteracoes = 0
    listaCaptura = []
    horas = []

    if CONEXAO:
        while (dados[1] < 24):
            if(quantidade_iteracoes < 3):
                listaCaptura.append ({
                    "graus": dados[0],
                    "data_atual": f"2024-03-16 {dados[1]}:{dados[2]}:00"
                    })
                horas.append(f"{dados[1]}:{dados[2]}")
                quantidade_iteracoes += 1
            else:
                inserir_dados(CONEXAO, listaCaptura)
                quantidade_iteracoes = 1

            dados = dados_simulados(dados[0], dados[1], dados[2])    

        temperaturas = [captura["graus"] for captura in listaCaptura]
        horas = [captura["data_atual"].split()[1].split(":")[0] for captura in listaCaptura]
        gerar_grafico(temperaturas, horas)

AMBIENTE_DOCKER = False
capturar_dados(AMBIENTE_DOCKER)
