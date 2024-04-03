import math
import random
import networkx as nx
import matplotlib.animation as animation
import matplotlib.pyplot as plt
class Vertice:
    def __init__(self, dado):
        self.dado = dado
        self.conectados = []
        self.grau = 0
class Aresta:
    def __init__(self, vertice1, vertice2):
        self.vertice1 = vertice1
        self.vertice2 = vertice2
class Grafo:
    def __init__(self, dados, vizinhos):
        self.maiorGrau = 0
        self.menorGrau = math.inf
        self.V = []
        self.E = []
        for dado in dados:
            verticeAdd = Vertice(dado)
            for vizinho in vizinhos:
                if dado == vizinho[0]:
                    verticeAdd.conectados.append(vizinho[1])
                elif dado == vizinho[1]:
                    verticeAdd.conectados.append(vizinho[0])
            self.V.append(verticeAdd)
        for vizinho in vizinhos:
            for i in range(0, len(self.V)):
                if self.V[i].dado == vizinho[0] and self.V[i].dado == vizinho[1]:
                    aresta= Aresta(self.V[i],self.V[i])
                    self.E.append(aresta)
                    self.V[i].grau+=1
                    continue
                elif self.V[i].dado ==vizinho[0]:
                    dadoProcurado = vizinho[1]
                elif self.V[i].dado == vizinho[1]:
                    dadoProcurado = vizinho[0]
                else:
                    continue
                for j in range(i+1, len(self.V)):
                    if self.V[j].dado == dadoProcurado:
                        aresta = Aresta(self.V[i], self.V[j])
                        self.E.append(aresta)
                        self.V[i].grau += 1
                        self.V[j].grau += 1
        for vertice in self.V:
            if vertice.grau > self.maiorGrau:
                self.maiorGrau = vertice.grau
            if vertice.grau < self.menorGrau:
                self.menorGrau = vertice.grau
        self.matrizDeAdjacencia()
        self.matrizDeIncidencia()
        self.listaIndexada()
        #Não poderia colocar que é instância de Grafo, pois todo Grafo é um Fecho(Polimorfismo)
        if not(isinstance(self,Fecho)):
            self.fecho = Fecho(dados,vizinhos)
            self.fecho.fechoHamiltoniano()
            #Setando todos os atributos do Fecho
            self.fecho.matrizDeAdjacencia()
            self.fecho.matrizDeIncidencia()
            self.fecho.listaIndexada()
            self.fecho.maiorGrau=0
            self.fecho.menorGrau=math.inf
            self.cicloEuleriano = self.Euleriano()
            for vertice in self.fecho.V:
                if vertice.grau > self.fecho.maiorGrau:
                    self.fecho.maiorGrau = vertice.grau
                if vertice.grau < self.fecho.menorGrau:
                    self.fecho.menorGrau = vertice.grau


    def exibirGraus(self):
        maior = []
        menor = []
        for vertice in self.V:
            if vertice.grau == self.maiorGrau:
                maior.append(vertice.dado)
            if vertice.grau == self.menorGrau:
                menor.append(vertice.dado)
        print(f"Maior(es) Grau(s): {maior}")
        print(f"Menor(es) Grau(s): {menor}")

    def matrizDeAdjacencia(self):
        self.MA = [] # Matriz de Adjacência
        for vertice in self.V:
            linha = []
            for vertice2 in self.V:
                if vertice.dado in vertice2.conectados or vertice2.dado in vertice.conectados:
                    linha.append(1)
                else:
                    linha.append(0)
            self.MA.append(linha)

    def exibirMA(self):
        for linha in self.MA:
            print(linha)

    def matrizDeIncidencia(self):
        self.MI = [] # Matriz de Incidência
        for vertice in self.V:
            linha = []
            for aresta in self.E:
                if vertice.dado == aresta.vertice1.dado or vertice.dado == aresta.vertice2.dado:
                    linha.append(1)
                else:
                    linha.append(0)
            self.MI.append(linha)

    def exibirMI(self):
        for linha in self.MI:
            print(linha)

    #Lista indexada
    def listaIndexada(self):
        self.LI = [] # Lista Indexada
        alfa = []
        indice=0 #indice do primeiro vértice
        alfa.append(indice)
        beta = []
        # alfa
        for i in range(0, len(self.V)):
            indice += (self.V[i].grau)
            alfa.append(indice)
        #beta
        for i in range(0,len(self.V)+1):
            if i==len(self.V):
                beta.append([])
                break
            for conectado in self.V[i].conectados:
                beta.append(conectado)
        self.LI.append([alfa, beta])
    def exibirLI(self):
        for item in self.LI:
            print(item)

    def addV(self, vertice):
        self.V.append(vertice)
        self.matrizDeAdjacencia()
        self.matrizDeIncidencia()
        self.listaIndexada()
        return vertice

    def addE(self, v1, v2):
        self.E.append(Aresta(v1, v2))
        v1.grau+=1
        v2.grau+=1
        self.matrizDeAdjacencia()
        self.matrizDeIncidencia()
        self.listaIndexada()

    #histograma
    # def plot_histograma(self):
    #     dadosX = [vertice.dado for vertice in self.V]
    #     dadosY = [vertice.grau for vertice in self.V]
    #     plt.bar(dadosX, dadosY,align="center")
    #     plt.xlabel('Vértices')
    #     plt.ylabel('Grau dos Vértices')
    #     plt.title('Histograma de Grau dos Vértices')
    #     plt.yticks(range(0, self.maiorGrau + 1))
    #     plt.grid(True)
    #     plt.show()
        #Dirac
    def Dirac(self):
        if len(self.V)>= 3 and self.menorGrau>=((len(self.V)/2)):
            return True
        else:
            return False

    def Ore(self):
        for i in range(0,len(self.V)):
            for j in range(i+1,len(self.V)):
                if self.V[i].dado not in self.V[j].conectados:
                    somaGraus = self.V[i].grau + self.V[j].grau
                    if somaGraus<len(self.V):
                        return False
        return True
    def BondyEChvatal(self):
        for vertice in self.fecho.V:
            if vertice.grau!=(len(self.V)-1):
                return False
        return True
    def Euleriano(self):
        cont=0
        for vertice in self.V:
            if vertice.grau%2 != 0:
                cont+=1
        if cont==2:
            #SemiEuleriano
            return 1;
        elif cont>2:
            #Não é SemiEuleriano
            return 0;
        else:
            #é Euleriano
            return 2
    def ciclo_ou_caminho(self):
        if self.cicloEuleriano==0:
            print("O Grafo não possui Ciclos nem Caminhos")
            return None
        elif self.cicloEuleriano==1:
            print("Semi-Euleriano")
            caminho = self.caminho()
            for i in range(0, len(caminho)):
                if i == len(caminho) - 1:
                    print(caminho[i].dado)
                else:
                    print(f"{caminho[i].dado}->", end='')

        else:
            print("Euleriano")
            ciclo = self.ciclo()
            for i in range(0, len(ciclo)):
                if i == len(ciclo) - 1:
                    print(ciclo[i].dado)
                else:
                    print(f"{ciclo[i].dado}->", end='')

    def caminho(self):
        # Garantindo que há 2 Vértices de Grau Impar(Em tese já foi filtrado, mas pode ser que o método seja execuado por fora)
        if self.cicloEuleriano == 1:
            indice=0
            verticeInicial=self.V[indice]
            while(verticeInicial.grau % 2==0):
                indice+=1
                verticeInicial = self.V[indice]
            #No final o vertice Inicial terá um grau ímpar
            #Copiando a lista de arestas
            arestas=self.E.copy()
            return self.continuidadeCaminho([verticeInicial],verticeInicial,arestas)
    def continuidadeCaminho(self,percurso,verticeAtual,arestasDisponiveis):
        if len(arestasDisponiveis)==0:
            return percurso
        else:
            for aresta in arestasDisponiveis:
                #O vertice está na aresta pesquisada?
                if aresta.vertice1.dado==verticeAtual.dado or aresta.vertice2.dado==verticeAtual.dado:
                    if aresta.vertice1.dado==verticeAtual.dado:
                        verticeAtual = aresta.vertice2
                    else:
                        verticeAtual = aresta.vertice1
                    percurso.append(verticeAtual)
                    #Não pode passar novamente por essa aresta
                    arestasDisponiveis.remove(aresta)
                    break
            return self.continuidadeCaminho(percurso,verticeAtual,arestasDisponiveis)
    def ciclo(self):
        #Garantindo que todos os Graus são pares
        if self.cicloEuleriano == 2:
            #Escolhendo aleatoriamente um vertice
            verticeInicial=self.V[random.randint(0,len(self.V)-1)]
            # Copiando a lista de arestas
            arestas = self.E.copy()
            return self.continuidadeCiclo([verticeInicial],verticeInicial,arestas)
    def continuidadeCiclo(self,ciclo,verticeAtual,arestasDisponiveis):
        if len(arestasDisponiveis)==0:
            if verticeAtual.dado == ciclo[0].dado:
                return ciclo
            else:
                #Reiniciando
                return self.ciclo()
        else:
            aresta = arestasDisponiveis[random.randint(0,len(arestasDisponiveis)-1)]
            #ALEATÓRIO
            while aresta.vertice1.dado not in verticeAtual.conectados and aresta.vertice2.dado not in verticeAtual.conectados:
                  aresta = arestasDisponiveis[random.randint(0, len(arestasDisponiveis) - 1)]
            if verticeAtual.dado == aresta.vertice1.dado:
                 verticeAtual = aresta.vertice2
            else:
                 verticeAtual = aresta.vertice1
            #SEQUENCIAL
            # for aresta in arestasDisponiveis:
            #     if aresta.vertice1.dado in verticeAtual.conectados or aresta.vertice2.dado in verticeAtual.conectados:
            #         if verticeAtual.dado == aresta.vertice1.dado:
            #             verticeAtual = aresta.vertice2
            #         else:
            #             verticeAtual = aresta.vertice1
            #         break
            ciclo.append(verticeAtual)
            # Não pode passar novamente por essa aresta
            arestasDisponiveis.remove(aresta)
            return self.continuidadeCiclo(ciclo,verticeAtual,arestasDisponiveis)
class Fecho(Grafo):
    def fechoHamiltoniano(self):
        #Montando o Fecho Hamiltoniano
        for i in range(0,len(self.V)):
            for j in range(i+1,len(self.V)):
                if self.V[i].dado not in self.V[j].conectados:
                    if (self.V[i].grau + self.V[j].grau)>=len(self.V):
                        self.addE(self.V[i],self.V[j])
                        self.V[i].conectados.append(self.V[j].dado)
                        self.V[j].conectados.append(self.V[i].dado)
        #Existem Pares de Vertices não Adjacentes cujos Graus somados dão pelo menos n?
        for i in range(0,len(self.V)):
            for j in range(i+1,len(self.V)):
                if not(self.V[i].dado in self.V[j].conectados):
                    if ((self.V[i].grau + self.V[j].grau) >= len(self.V)):
                        self.fechoHamiltoniano()
#Main
#Grafos
pontos = [1,2,3,4,5,6,7]
ligacoes1 = [[1,2],[1,3],[1,6],[1,7],[2,3],[2,4],[2,6],[3,4],[3,5],[4,5],[4,7],[5,6],[5,7],[6,7]]
ligacoes2 = [[1,2],[1,3],[1,6],[1,7],[2,3],[2,4],[2,6],[3,4],[4,5],[4,7],[5,6],[5,7],[6,7]]
ligacoes3 = [[1,2],[1,3],[1,6],[1,7],[2,3],[3,4],[4,5],[5,6],[5,7],[6,7]]
ligacoes4 = [[1,2],[1,3],[1,6],[1,7],[2,3],[3,4],[4,5],[5,6],[6,7]]
grafo1 = Grafo(pontos,ligacoes1)
grafo2 = Grafo(pontos,ligacoes2)
grafo3 = Grafo(pontos,ligacoes3)
grafo4 = Grafo(pontos,ligacoes4)
print("Grafo 1:")
grafo1.ciclo_ou_caminho()
print("Grafo 2:")
grafo2.ciclo_ou_caminho()
print("Grafo 3:")
grafo3.ciclo_ou_caminho()
print("Grafo 4:")
grafo4.ciclo_ou_caminho()