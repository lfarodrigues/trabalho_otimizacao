import random
import math

class Pessoa:
    def __init__(self, valor, peso):
        self.id = 0
        self.valor = valor
        self.peso = peso
class Aviao:
    def __init__(self, capacidade):
        self.capacidade = capacidade
        self.pessoas = [] # Integer arr
        self.peso_atual = 0
        self.valor_atual = 0

    def adicionar_pessoa(self, pessoa):
            self.pessoas.append(pessoa)
            self.peso_atual += pessoa.peso
            self.valor_atual += pessoa.valor

            # soma valor caso tenha relacao com alguem já dentro do aviao

    def remover_pessoa(self, index):
        self.peso_atual -= self.pessoas[index].peso
        self.valor_atual -= self.pessoas[index].valor
        return self.pessoas.pop(index)

class Instancia:
    def __init__(self, pessoas, quantidade_avioes, avioes, relacoes_amizade):
        self.quantidade_avioes = quantidade_avioes
        self.pessoas = pessoas
        self.avioes = avioes
        self.relacoes_amizade = relacoes_amizade

    def adicionar_pessoa(self, pessoa):
        self.pessoas.append(pessoa)

    def remover_pessoa(self, index):
        if 0 <= index < len(self.pessoas):
            del self.pessoas[index]
        else:
            print("Índice inválido. Não é possível remover a pessoa.")
    
    def adicionar_aviao(self, aviao):
        self.avioes.append(aviao)

    def remover_aviao(self, index):
        if 0 <= index < len(self.avioes):
            del self.avioes[index]
        else:
            print("Índice inválido. Não é possível remover o avião.")

class Solucao:
    def __init__(self, pessoas_selecionadas, avioes, relacoes_amizade):
        self.pessoas_selecionadas = pessoas_selecionadas
        self.avioes = avioes
        self.relacoes_amizade = relacoes_amizade
        self.valor  = 0

        self.calcular_valor_total()

    # agraga valor de cada aviao mais o custo das relacoes de amizade
    def calcular_valor_total(self):
        for aviao in self.avioes:
            self.valor += aviao.valor_atual
            for i in range(0, len(aviao.pessoas) - 1):
                for j in range(i + 1, range(len(aviao.pessoas) - 1)):
                    pessoa1 = aviao.pessoas[i].id
                    pessoa2 = aviao.pessoas[j].id
                    self.valor += self.relacoes_amizade[pessoa1][pessoa2] 
                


# Lê uma instância do arquivo nome_arquivo
def le_instancia(nome_arquivo):
    with open(nome_arquivo, 'r') as f:
        linhas = f.readlines()
    
    numero_pessoas = int(linhas[0])
    valores_pessoas = list(map(int, linhas[1].split()))
    relacoes_amizade = [list(map(int, linha.split())) for linha in linhas[2:numero_pessoas+2]]
    pesos_pessoas = list(map(int, linhas[4 + numero_pessoas].split()))

    pessoas = [Pessoa(valor, peso) for valor, peso in zip(valores_pessoas, pesos_pessoas)]

    last_id = 0
    for pessoa in pessoas:
        pessoa.id = last_id + 1

    avioes = []
    m = 10
    capacidade_total = sum(pesos_pessoas)
    capacidade_por_aviao = int(0.8 / m * capacidade_total)    
    for _ in range(1, 10):
        avioes.append(Aviao(capacidade_por_aviao))
    
    return Instancia(pessoas, avioes, relacoes_amizade)    

def criar_solucao_inicial(instancia):
    pessoas_ordenadas = sorted(instancia.pessoas, key=lambda pessoa: pessoa.valor, reverse=True)
    pessoas_selecionadas = []

    # Adiciona pessoas com maior valor disposto a pagar primeiro
    for aviao in instancia.avioes:
        peso_disponivel = aviao.capacidade - aviao.peso_atual
        if peso_disponivel <= 0:
            continue

        if len(pessoas_ordenadas) > 0:
            for pessoa in pessoas_ordenadas:
                if pessoa.peso <= peso_disponivel:
                    aviao.adicionar_pessoa(pessoa.id)
                    peso_disponivel -= pessoa.peso
                    pessoas_selecionadas.append(pessoa)
                    pessoas_ordenadas.remove(pessoa)
                else:
                    break
        else:
            break
    return Solucao(pessoas_selecionadas, instancia.avioes, instancia.relacoes_amizade)

def vizinhanca(sol):
    nova_sol = Solucao(sol.pessoas_selecionadas.copy(), sol.avioes, sol.relacoes_amizade)
    pessoa_index = random.randint(0, len(nova_sol.pessoas_selecionadas) - 1)
    novo_aviao_index = random.randint(0, len(nova_sol.avioes) - 1)
    nova_sol.pessoas_selecionadas[pessoa_index] = novo_aviao_index * len(nova_sol.avioes) + pessoa_index % len(nova_sol.avioes)
    return nova_sol

def simulated_annealing(instancia, temperatura_inicial, temperatura_final, taxa_resfriamento, iteracoes_por_temperatura):
    sol_corrente = criar_solucao_inicial(instancia)
    melhor_sol = sol_corrente

    temperatura = temperatura_inicial
    while temperatura > temperatura_final:
        for _ in range(iteracoes_por_temperatura):
            nova_sol = vizinhanca(sol_corrente)
            delta = nova_sol.valor - sol_corrente.valor
            if delta > 0 or random.random() < math.exp(delta / temperatura):
                sol_corrente = nova_sol
                if nova_sol.valor > melhor_sol.valor:
                    melhor_sol = nova_sol
        temperatura *= taxa_resfriamento

    return melhor_sol

# Teste
instancia = le_instancia('instances/vf01.dat')
solucao = simulated_annealing(instancia, 100, 0.01, 0.9, 1000)
print(solucao)
