import capturarDados
import enums

if __name__ == "__main__":
    AMBIENTE = enums.AMBIENTE_DOCKER

    if AMBIENTE == enums.AMBIENTE_DOCKER or AMBIENTE == enums.AMBIENTE_LOCAL:
        capturarDados.capturar_dados(AMBIENTE)
    elif AMBIENTE == enums.IOTHUB:
        capturarDados.enviar_dados_iot(AMBIENTE)
    else:
        print("Ambiente não definido.")