import conexaoBanco as conexao
import visualizacao
import time
import datetime
import random

def capturar_dados(AMBIENTE_DOCKER):
    CONEXAO = conexao.conectar_bd(AMBIENTE_DOCKER)
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
                conexao.inserir_dados(CONEXAO, listaCaptura)
                visualizacao.relacao_temperatura_tempo(listaCaptura)
                listaCaptura.clear()
                quantidade_iteracoes = 0

            time.sleep(ATRASO)
            