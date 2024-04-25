import capturarDados

if __name__ == "__main__":
    AMBIENTE_DOCKER = False

    if AMBIENTE_DOCKER:
        capturarDados.capturar_dados_sql()
    else:
        capturarDados.capturar_dados_iot()