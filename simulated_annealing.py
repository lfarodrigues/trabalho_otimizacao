import random
import math
import time
from copy import copy

n_pessoas = 0
m = 10
class Pessoa:
    def __init__(self, valor, peso):
        self.id = 0
        self.valor = valor
        self.peso = peso
class Aviao:
    def __init__(self, capacidade):
        self.capacidade = capacidade
        self.pessoas = [] # Pessoa arr
        self.peso_atual = 0
        self.valor_atual = 0

    def adicionar_pessoa(self, pessoa):
        self.pessoas.append(pessoa)
        self.peso_atual += pessoa.peso
        self.valor_atual += pessoa.valor
    
    def pessoa_no_aviao(self, id):
        return id in self.pessoas
        # soma valor caso tenha relacao com alguem já dentro do aviao
   
    def encontrar_indice_pessoa_menor_relacao_valor_peso(self):
        menor_relacao_valor_peso = float('inf')
        indice_pessoa_menor_relacao_valor_peso = None
        
        for i, pessoa in enumerate(self.pessoas):
            relacao_valor_peso = pessoa.valor / pessoa.peso
            if relacao_valor_peso < menor_relacao_valor_peso:
                menor_relacao_valor_peso = relacao_valor_peso
                indice_pessoa_menor_relacao_valor_peso = i
        
        return indice_pessoa_menor_relacao_valor_peso
        
    def imprime_pessoas(self):
        print("\n")
        print("Pessoas no aviao")
        for pessoa in self.pessoas:
            print("Id:", pessoa.id, "Valor:", pessoa.valor, "Peso:", pessoa.peso, end=' ')
        print("\n")
        return
    
    def remover_pessoa_id(self, id):
        for pessoa in self.pessoas:
            if pessoa.id == id:
                self.pessoas.remove(pessoa)
                return

    def remover_pessoa(self, index):
        self.peso_atual -= self.pessoas[index].peso
        self.valor_atual -= self.pessoas[index].valor
        return self.pessoas.pop(index)

    def calcula_valor(self):
        return sum(pessoa.valor for pessoa in self.pessoas)

    def calcula_peso(self):
        return sum(pessoa.peso for pessoa in self.pessoas)
class Instancia:
    def __init__(self, pessoas, avioes, relacoes_amizade):
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
        self.valor = 0
        for aviao in self.avioes:
            #print("Peso no aviao:", aviao.peso_atual)
            self.valor += aviao.calcula_valor() + calcula_custo_relacoes(aviao.pessoas, self.relacoes_amizade)
                
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
        pessoa.id = last_id
        last_id += 1

    avioes = []
    capacidade_total = sum(pesos_pessoas)
    capacidade_por_aviao = int((0.8 / m) * capacidade_total) 
    for _ in range(m):
        avioes.append(Aviao(capacidade_por_aviao))
    
    return Instancia(pessoas, avioes, relacoes_amizade)    

# Calcula o custo da relacao entre pessoas num mesmo aviao
def calcula_custo_relacoes(lista_pessoas, matriz_relacoes):
    custo_relacoes = 0
    #print("Numero de pessoas no aviao", len(lista_pessoas))
    if len(lista_pessoas) > 0:
        for i in range(0, len(lista_pessoas) - 1):
            for j in range(i + 1, len(lista_pessoas) - 1):
                pessoa1 = lista_pessoas[i].id
                pessoa2 = lista_pessoas[j].id

                custo_relacao = 0

                if pessoa1 > pessoa2:
                    temp = pessoa2
                    pessoa2 = pessoa1
                    pessoa1 = temp

                diff_cols = pessoa1 + 1
                coluna = pessoa2 - diff_cols
                
                custo_relacao = matriz_relacoes[pessoa1][coluna]

                custo_relacoes += custo_relacao

    return custo_relacoes

# Cria uma solução inicial fazendo a escolha gulosa de pessoas com maior valor disposto a pagar
def criar_solucao_inicial(instancia):   
    # Ordenar pessoas pela relação valor/peso
    pessoas_ordenadas = sorted(instancia.pessoas, key=lambda pessoa: int(pessoa.valor / pessoa.peso), reverse=True)
    pessoas_selecionadas = []
    
    for aviao in instancia.avioes:
        for pessoa in pessoas_ordenadas:
            if (aviao.calcula_peso() + pessoa.peso) <= aviao.capacidade:
                aviao.pessoas.append(pessoa)
                pessoas_selecionadas.append(pessoa.id)
                pessoas_ordenadas.remove(pessoa)

    return Solucao(pessoas_selecionadas, instancia.avioes, instancia.relacoes_amizade)

def obtem_todos_ids_pessoas(avioes):
    lista_ids = []
    for aviao in avioes:
        for pessoa in aviao.pessoas:
            lista_ids.append(pessoa.id)
    return lista_ids

def calcula_valor_pessoa(pessoa, lista_pessoas, matriz_relacoes):
    valor_pessoa = pessoa.valor
    # calcula o valor das relacoes
    if len(lista_pessoas) > 0:
        for j in range(0, len(lista_pessoas) - 1):
            if lista_pessoas[j].id == pessoa.id:
                continue
            pessoa1 = pessoa.id
            pessoa2 = lista_pessoas[j].id

            custo_relacao = 0

            if pessoa1 > pessoa2:
                temp = pessoa2
                pessoa2 = pessoa1
                pessoa1 = temp

            diff_cols = pessoa1 + 1
            coluna = pessoa2 - diff_cols
            
            custo_relacao = matriz_relacoes[pessoa1][coluna]

            valor_pessoa += custo_relacao
    return valor_pessoa

# Escolhe pessoas em avioes diferentes para serem trocadas
def vizinhanca_aleatoria(sol):
    nova_sol = Solucao(sol.pessoas_selecionadas.copy(), sol.avioes, sol.relacoes_amizade)
    num_avioes = len(sol.avioes)

    # Seleciona um avião aleatório
    aviao1 = random.randrange(num_avioes)

    # Seleciona uma pessoa aleatória do avião selecionado
    indice_pessoa1 = random.randrange(len(nova_sol.avioes[aviao1].pessoas))
    pessoa1 = nova_sol.avioes[aviao1].pessoas[indice_pessoa1]

    # Seleciona outro avião diferente do avião selecionado
    aviao2 = (aviao1 + random.randint(1, num_avioes - 1)) % num_avioes

    # Seleciona uma pessoa aleatória do avião selecionado
    indice_pessoa2 = random.randrange(len(nova_sol.avioes[aviao2].pessoas))
    pessoa2 = nova_sol.avioes[aviao2].pessoas[indice_pessoa2]
    
    # Calcula a capacidade após a troca
    capacidade_aviao1 = nova_sol.avioes[aviao1].capacidade
    capacidade_aviao2 = nova_sol.avioes[aviao2].capacidade

    novo_peso_aviao1= nova_sol.avioes[aviao1].calcula_peso() - pessoa1.peso + pessoa2.peso
    novo_peso_aviao2 = nova_sol.avioes[aviao2].calcula_peso() - pessoa2.peso + pessoa1.peso

    # Verifica se a capacidade é respeitada para ambos os aviões
    if novo_peso_aviao1 <= capacidade_aviao1 and novo_peso_aviao2 <= capacidade_aviao2:
        nova_sol.avioes[aviao1].remover_pessoa(indice_pessoa1)
        nova_sol.avioes[aviao2].remover_pessoa(indice_pessoa2)

        nova_sol.avioes[aviao1].adicionar_pessoa(pessoa2)
        nova_sol.avioes[aviao2].adicionar_pessoa(pessoa1)

    nova_sol.calcular_valor_total()

    return nova_sol

def vizinhanca_troca_pessoas_selecionadas(sol_atual, pessoas_instancia):
    # Copiar as pessoas já selecionadas da solução atual
    pessoas_selecionadas = sol_atual.pessoas_selecionadas.copy()
    avioes = sol_atual.avioes
    num_avioes = len(sol_atual.avioes)

    lista_todos_ids = obtem_todos_ids_pessoas(avioes)
    # Encontrar pessoas não selecionadas na instância
    pessoas_nao_selecionadas = [pessoa for pessoa in pessoas_instancia if pessoa.id not in lista_todos_ids]
    
    # Escolher o avião aleatoriamente
    indice_aviao = random.randrange(num_avioes)
    aviao = avioes[indice_aviao]

    # Calcula total agregado do aviao
    total_atual = aviao.calcula_valor() + calcula_custo_relacoes(aviao.pessoas, sol_atual.relacoes_amizade)
    
    #time.sleep(10)
    #aviao.imprime_pessoas()
    #time.sleep(10)

    if pessoas_nao_selecionadas:
        # Seleciona uma pessoa que ainda nao foi selecionada
        for pessoa_nova in pessoas_nao_selecionadas:
            for pessoa_aviao in aviao.pessoas:
                custo_pessoa_aviao = calcula_valor_pessoa(pessoa_aviao, aviao.pessoas, sol_atual.relacoes_amizade) # Valor pessoa + Relacoes de amizade
                aviao.remover_pessoa_id(pessoa_aviao.id)
                custo_pessoa_nova = calcula_valor_pessoa(pessoa_nova, aviao.pessoas, sol_atual.relacoes_amizade)

                # Se aumenta valor agregado e o aviao comporta a pessoa
                if (custo_pessoa_nova > custo_pessoa_aviao) and (aviao.calcula_peso() + pessoa_nova.peso <= aviao.capacidade) :
                    aviao.adicionar_pessoa(pessoa_nova)
                    avioes[indice_aviao] = aviao
                    return Solucao(pessoas_selecionadas, avioes, sol_atual.relacoes_amizade)
                # se nao volta com a pessoa que ja estava
                aviao.adicionar_pessoa(pessoa_aviao)
    return sol_atual

def simulated_annealing(solucao_ini, temperatura_inicial, temperatura_final, taxa_resfriamento, iteracoes_por_temperatura):
    sol_corrente = solucao_ini
    melhor_sol = sol_corrente

    print("Valor solução inicial", melhor_sol.valor)

    temperatura = temperatura_inicial
    while temperatura > temperatura_final:
        for _ in range(iteracoes_por_temperatura):
            nova_sol = vizinhanca_aleatoria(sol_corrente)
            delta = nova_sol.valor - sol_corrente.valor
            if delta > 0 or random.random() < math.exp(delta / temperatura):
                sol_corrente = nova_sol
                if nova_sol.valor > melhor_sol.valor:
                    melhor_sol = nova_sol
        temperatura *= taxa_resfriamento

    return melhor_sol

def simulated_annealing_2(instancia, solucao_ini, temperatura_inicial, temperatura_final, taxa_resfriamento, iteracoes_por_temperatura):
    sol_corrente = solucao_ini
    melhor_sol = sol_corrente

    print("Valor solução inicial", melhor_sol.valor)

    temperatura = temperatura_inicial
    while temperatura > temperatura_final:
        for _ in range(iteracoes_por_temperatura):
            nova_sol = vizinhanca_troca_pessoas_selecionadas(sol_corrente, instancia.pessoas)
            delta = nova_sol.valor - sol_corrente.valor
            if delta > 0 or random.random() < math.exp(delta / temperatura):
                sol_corrente = nova_sol
                if nova_sol.valor > melhor_sol.valor:
                    melhor_sol = nova_sol
        temperatura *= taxa_resfriamento

    return melhor_sol

def mostra_resultado(solucao):
    i = 1
    for aviao in solucao.avioes:
        ids = []
        valores = []
        pesos = []
        for pessoa in aviao.pessoas:
            ids.append(pessoa.id)
            valores.append(pessoa.valor)
            pesos.append(pessoa.peso)
        print(f"Alocação de pessoas no aviao {i}:", ids)
        print(f"Valores no aviao {i}:", valores)
        print(f"Pesos no aviao {i}:", pesos)

        i+=1
        
    print("Valor da melhor solucao encontrada:", solucao.valor)
    return

instancia = le_instancia('instances/vf01.dat')
solucao_ini = criar_solucao_inicial(instancia)
#print(sol_ini.valor)
#solucao = simulated_annealing(solucao_ini, 1000, 0.01, 0.95, 1000)  # Primeiro realizamos a otimizacao com troca entre avioes
solucao2 = simulated_annealing_2(instancia, solucao_ini, 5000, 0.01, 0.95, 5000) # Tentamos melhorar ainda mais a solucao alocando pessoas nao selecionandas  
mostra_resultado(solucao2)