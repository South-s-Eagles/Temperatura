import conexaoBanco as conexao
import visualizacao
import time
import datetime
import random
import json

from azure.iot.device import IoTHubDeviceClient, Message

def capturar_dados_sql():
    CONEXAO = conexao.conectar_bd()
    quantidade_iteracoes = 0
    listaCaptura = []
    ATRASO = 60*2 # Intervalo de captura de dados (em segundos)

    if CONEXAO:
        bateria = 100
        while True:
            if(quantidade_iteracoes < 2):
                listaCaptura.append ({
                    "graus": random.uniform(15, 35),
                    "data_atual": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    })
                quantidade_iteracoes += 1
            else:
                conexao.inserir_dados(CONEXAO, listaCaptura, bateria)
                visualizacao.relacao_temperatura_tempo(listaCaptura)
                listaCaptura.clear()
                quantidade_iteracoes = 0
            
            bateria -= 1
            time.sleep(ATRASO)

def capturar_dados_iot():
    ATRASO = 60*2 # Intervalo de captura de dados (em segundos)
    bateria = 100.0
    graus = "{:.2f}".format(random.uniform(35.97, 36.5))
    horas = 0
    minutos = 0

    while True:
        dados_simulados(graus, horas, minutos)
        enviar_dados_iot(graus, bateria)

        bateria -= 0.1
        time.sleep(ATRASO)

def enviar_dados_iot(GRAUS, BATERIA):
    CONNECTION_STRING = "HostName=helder03221027.azure-devices.net;DeviceId=helder03221027;SharedAccessKey=98lTBFzWpGkLzoZRzC/B5pkRbEqupSMjqAIoTMXu7iI="
    DEVICE_ID = "helder03221027"
    
    try:
        client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

        payload = {
            "device_id": DEVICE_ID,
            "graus": GRAUS,
            "bateria": BATERIA
        }

        message = Message(json.dumps(payload))

        client.send_message(message)
        print("Mensagem enviada para o IoT Hub:", message)
    except Exception as e:
        print("Erro ao enviar mensagem para o IoT Hub:", e)
        return
    
def dados_simulados(graus, hora, minuto):
    if (hora == 14 and minuto == 0) or (hora == 16 and minuto == 0) or (hora == 18 and minuto == 0):
        graus += random.uniform(1.1, 1.5)
    else:
        if hora < 8 and graus > 36.2:
            graus -= random.uniform(0.1, 0.5)
        elif hora >= 8 and hora < 14 and graus > 36.9:
            graus -= random.uniform(0.1, 0.5)
        elif hora >= 14 and hora < 18 and graus > 37.2:
            graus -= random.uniform(0.1, 0.5)
        elif hora >= 18 and graus > 36.5:
            graus -= random.uniform(0.1, 0.5)
        else:
            graus += random.uniform(0.1, 0.5)

    if minuto >= 58:
        hora += 1
        minuto = 0
    else:
        minuto += 2

    return graus, hora, minuto