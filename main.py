import mysql.connector
import datetime
import json
import random
import time
from azure.iot.device import IoTHubDeviceClient, Message

def conectar_bd():
    HOST = "localhost"
    USER = "root"
    PORT = "3306"
    PASSWORD = "root"
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

def inserir_dados(CONEXAO, graus, bateria):
    agora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        cursor = CONEXAO.cursor()
        cursor.execute(
            "INSERT INTO temperatura (graus, data) VALUE({}, '{}');"
            .format(graus, agora)
            )
        cursor.execute(
            "INSERT INTO sensor (bateria, data) VALUE ({}, '{}');"
            .format(bateria, agora)
            )
        CONEXAO.commit()
        cursor.close()
        print("Dados inseridos com sucesso.")
    except Exception as e:
        print(f"Erro ao inserir dados: {e}")

def simulador(graus):
    agora = datetime.datetime.now().strftime("%H:%M")
    if (agora == "14:00") or (agora == "16:00") or (agora == "18:00"):
        graus += random.uniform(1.1, 1.3)
    else:
        if agora < "08:00" and graus > 36.2:
            graus -= random.uniform(0.1, 0.4)
        elif agora >= "08:00" and agora < "14:00" and graus > 36.9:
            graus -= random.uniform(0.1, 0.4)
        elif agora >= "14:00" and agora < "18:00" and graus > 37.2:
            graus -= random.uniform(0.1, 0.4)
        elif agora >= "18:00" and graus > 36.5:
            graus -= random.uniform(0.1, 0.4)
        else:
            graus += random.uniform(0.1, 0.4)

        return graus

def captura():
    CONNECTION_STRING = "HostName=helder03221027.azure-devices.net;DeviceId=helder03221027;SharedAccessKey=98lTBFzWpGkLzoZRzC/B5pkRbEqupSMjqAIoTMXu7iI="
    DEVICE_ID = "helder03221027"
    graus = random.uniform(35.97, 36.5)
    CONEXAO = conectar_bd()
    ATRASO = 60*2 # Intervalo de captura de dados (em segundos)
    bateria = 100.0

    while True:
        graus = simulador(graus)
        bateria -= 0.1
        
        # inserir_dados(CONEXAO, graus, bateria)
        
        try:
            client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
            payload = {
                "device_id": DEVICE_ID,
                "graus": round(graus, 2),
                "bateria": round(bateria, 2)
            }

            message = Message(json.dumps(payload))

            client.send_message(message)
            client.disconnect()
            print("Mensagem enviada para o IoT Hub:", message)
        except Exception as e:
            print("Erro ao enviar mensagem para o IoT Hub:", e)
        
        time.sleep(ATRASO)

captura()