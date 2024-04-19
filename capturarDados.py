import conexaoBanco as conexao
import visualizacao
import time
import datetime
import random
import json

from azure.iot.device import IoTHubDeviceClient, Message

def capturar_dados(AMBIENTE):
    CONEXAO = conexao.conectar_bd(AMBIENTE)
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

def enviar_dados_iot(graus, bateria):
    CONNECTION_STRING = "HostName=helder03221027.azure-devices.net;DeviceId=temperatura;SharedAccessKey=hO6jfKve16lnruQjqEiYIo9WNZAIoTCDUPreaI2nkEf="
    DEVICE_ID = "temperatura"

    try:
         client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

         payload = {
             "device_id": DEVICE_ID,
             "graus": graus,
             "bateria": bateria
         }

         message = Message(json.dumps(payload))

         client.send_message(message)
         print("Mensagem enviada para o IoT Hub:", message)
    except Exception as e:
        print("Erro ao enviar mensagem para o IoT Hub:", e)