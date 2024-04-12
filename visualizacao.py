import matplotlib.pyplot as plt

def temperatura_x_tempo(listaCaptura):
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