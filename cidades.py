from geneticos.individuo import Individuo
import csv
from random import randint
import sys

TEMPO_MAXIMO = 72
PESO_MAXIMO = 20

ITENS = [
    ["Coroa do Rei Joao II", 5, 10, 10000, "Santa Paula"],
    ["Espada sagrada", 6, 5, 6500, "Campos"],
    ["Cálice do Santo Graal", 2, 6, 7000, "Riacho de Fevereiro"],
    ["Colar de casamento da rainha Vanessa", 1, 7, 2500, "Algas"],
    ["Maior diamante do     continente", 2, 10, 5400, "Alem-do-Mar"],
    ["Primeira ediçao do livro O Livro Azul", 1, 2, 3000, "Guardiao"],
    ["Quadro do maior pintor do século", 4, 4, 2000, "Foz da Agua Quente"],
    ["Taça da Copa do Mundo de Corrida de Cavalo", 2, 5, 4000, "Leao"],
    ["Fóssil da primeira galinha conhecida", 2, 1, 2500, "Granada"],
    ["Primeira moeda de $1 do país", 1, 7, 3000, "Lagos"],
    ["Busto do líder da Revoluçao Pavao", 6, 5, 1500, "Ponte-do-Sol"],
    ["Fecha do caçador pré-histórico", 1, 2, 2300, "Porto"],
    ["Capacete de guerra antigo", 2, 4, 4000, "Limoes"]
]
ITEM = 0
PESO = 1
TEMPO_ROUBO = 2
VALOR = 3
CIDADE = 4

transporte = []
cidades = set()
with open('cidades.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)

    for row in reader:
        if (row[0] != "Escondidos"):
            cidades.add(row[0])
        if (row[1] != "Escondidos"):
            cidades.add(row[1])
        transporte.append({
            'origem': row[0],
            'destino': row[1],
            'tempo': int(row[2]),
            'custo': int(row[3])
        })
        transporte.append({
            'origem': row[1],
            'destino': row[0],
            'tempo': int(row[2]),
            'custo': int(row[3])
        })


def tempo_entre(origem, destino):
    for item in transporte:
        if (item['origem'] == origem and item['destino'] == destino):
            return item['tempo']
def custo_entre(origem, destino):
    for item in transporte:
        if (item['origem'] == origem and item['destino'] == destino):
            return item['custo']


def obter_peso_roubo(cidade):
    for item in ITENS:
        if item[CIDADE] == cidade:
            return item[PESO]


def obter_tempo_roubo(cidade):
    for item in ITENS:
        if item[CIDADE] == cidade:
            return item[TEMPO_ROUBO]


def obter_valor_roubo(cidade):
    for item in ITENS:
        if item[CIDADE] == cidade:
            return item[VALOR]


class Cidades(Individuo):
    escondidos = 'Escondidos'
    ADICIONAR_NOVA_CIDADE = 1
    TROCAR_CIDADES = 2

    def __init__(self, rota=None):
        if (rota is None):
            self.rota = self._rota_aleatoria()
        else:
            self.rota = rota
            self._gerar_pilha()

    # Menor tempo de rota e maior valor de itens
    # Não pode passar do peso ou tempo máximos
    def fitness(self):
        fitness = 0
        peso = 0
        tempo = 0
        valor = 0
        custo_transporte = 0

        for i in range(0, len(self.rota) - 2):
            tempo += tempo_entre(self.rota[i], self.rota[i + 1])
            custo_transporte += custo_entre(self.rota[i], self.rota[i + 1])
        for i in range(1, len(self.rota) - 2):
            tempo += obter_tempo_roubo(self.rota[i])
            peso += obter_peso_roubo(self.rota[i])
            valor += obter_valor_roubo(self.rota[i])
        valor -= custo_transporte
        
        if tempo > TEMPO_MAXIMO or peso > PESO_MAXIMO:
            return -sys.maxsize - 1

        fitness += tempo * -1
        fitness += valor

        return fitness

    def mutacao(self):
        nova_rota = self.rota.copy()

        method = randint(1, 2)
        if method == self.ADICIONAR_NOVA_CIDADE:
            if len(self.pilha_cidades) > 0:
                cidade = randint(0, len(self.pilha_cidades) - 1)
                proxima_cidade = self.pilha_cidades.pop(cidade)

                posicao = randint(1, len(nova_rota) - 2)
                nova_rota.insert(posicao, proxima_cidade)
            else:
                method = self.TROCAR_CIDADES
        if method == self.TROCAR_CIDADES:
            primeira = randint(1, len(nova_rota) - 2)
            segunda = randint(1, len(nova_rota) - 2)
            nova_rota[primeira], nova_rota[segunda] = nova_rota[segunda], nova_rota[primeira]

        return Cidades(nova_rota)

    def crossover(self, b):
        i = 1
        j = 1

        filho = [self.escondidos]
        while j < len(b.rota) - 2 and i < len(self.rota) - 2:
            select = randint(1, 2)
            if select == 1 and self.rota[i] not in filho:
                filho.append(self.rota[i])
            elif select == 2 and b.rota[j] not in filho:
                filho.append(b.rota[j])
            j += 1
            i += 1
        while j < len(b.rota)-2:
            if b.rota[j] not in filho:
                filho.append(b.rota[j])
            j += 1
        while i < len(self.rota) - 2:
            if self.rota[i] not in filho:
                filho.append(self.rota[i])
            i += 1

        filho.append(self.escondidos)
        return Cidades(filho)

    def imprime(self):
        peso = 0
        tempo = 0
        valor = 0

        for i in range(0, len(self.rota) - 2):
            tempo += tempo_entre(self.rota[i], self.rota[i + 1])
        for i in range(1, len(self.rota) - 2):
            tempo += obter_tempo_roubo(self.rota[i])
            peso += obter_peso_roubo(self.rota[i])
            valor += obter_valor_roubo(self.rota[i])
        print(self.rota)
        print("Valor: " + str(valor))
        print("Peso: " + str(peso))
        print("Tempo: " + str(tempo))

    def _rota_aleatoria(self):
        rota = []
        while True:
            rota.append(self.escondidos)
            tempo = 0
            peso = 0

            self.pilha_cidades = list(cidades.copy())
            while len(self.pilha_cidades) > 0:
                cidade = randint(0, len(self.pilha_cidades) - 1)
                proxima_cidade = self.pilha_cidades.pop(cidade)
                cidade_atual = rota[len(rota) - 1]

                tempo_proxima_cidade = tempo_entre(cidade_atual, proxima_cidade) + obter_tempo_roubo(proxima_cidade)
                estorou_tempo = tempo + tempo_proxima_cidade + tempo_entre(proxima_cidade,
                                                                           self.escondidos) > TEMPO_MAXIMO

                peso_proxima_cidade = obter_peso_roubo(proxima_cidade)
                estorou_peso = peso + peso_proxima_cidade > PESO_MAXIMO

                if estorou_tempo or estorou_peso:
                    self.pilha_cidades.append(proxima_cidade)
                    break
                else:
                    tempo += tempo_proxima_cidade
                    peso += peso_proxima_cidade
                    rota.append(proxima_cidade)

            cidade_atual = rota[len(rota) - 1]
            rota.append(self.escondidos)
            tempo += tempo_entre(cidade_atual, self.escondidos)

            if tempo <= TEMPO_MAXIMO:
                break
            rota = []

        return rota

    def _gerar_pilha(self):
        self.pilha_cidades = []
        for cidade in cidades:
            if cidade not in self.rota:
                self.pilha_cidades.append(cidade)
