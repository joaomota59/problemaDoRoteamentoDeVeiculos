from itertools import permutations
from igraph import *
from random import randint
import time

def forcaBruta():
    melhor_peso=0 #contém o valor do ciclo hamiltoniano de menor custo
    melhor_rota=[] #contém a melhor rota
    k=0
    arquivo = open("rotas.txt", "w")#apaga se ja tiver algo gravado // guarda no txt todas as rotas (hamitonianas) e seus pesos
    arquivo.close
    inicio = time.time()
    for subset in permutations([i for i in range(n)], n):#todas permutacões de rotas possíveis no caso gera (n-1)! rotas possíveis
        arquivo = open("rotas.txt", "a")
        if subset[0]==0:#pega as permutações de onde começa apenas do zero ou seja no caso é o depósito
            soma_peso_rota = 0  # calcula a soma do pesso da rota
            for i in range(n-1):
                soma_peso_rota += g.es.select(_source=subset[i], _target=subset[i+1])['weight'][0]
            soma_peso_rota+=g.es.select(_source=subset[i+1], _target=subset[0])['weight'][0]
            texto = str(list(subset)+list([0]))+" : "+str(soma_peso_rota)+"\n"
            arquivo.write(texto)
            if k == 0:
                melhor_peso = soma_peso_rota
                melhor_rota = list(subset)+list([0])
            elif soma_peso_rota < melhor_peso:
                melhor_peso = soma_peso_rota
                melhor_rota = list(subset)+list([0])
            k+=1
        else:
            arquivo.close()
            break

    fim = time.time()
    print("Tempo de execução:",fim - inicio,"segundos!")
    print("Peso da melhor rota:",melhor_peso)
    print("Melhor rota:",melhor_rota)
def VMP_Heuristica():
    global g
    grafo_aux=g
    H=[g.vs["name"][0]]#deposito incluido em H(conjunto)
    i=0#vertice inicial a ser analisado (depósito)
    id_melhor=None
    #peso_da_rota=0
    inicio = time.time()
    while len(H)<n:
        z=0
        for w in range(len(g.vs["name"])): #percorre o grafo e procura o vizinho mais proximo(menor peso) dado o vertice
            if i!=w: #o elemento que esta sendo analisado precisa ser diferente dele mesmo
                vizinho_mais_prox = g.es.select(_source=i, _target=w)['weight'][0]
                if z == 0:
                    melhor_peso = vizinho_mais_prox #guarda o peso da aresta com o melhor vizinho
                    melhor_vizinho = g.vs["name"][w] #pega o vértice do melhor vizinho
                    id_melhor = w # id do melhor vizinho
                elif vizinho_mais_prox < melhor_peso:
                    melhor_peso = vizinho_mais_prox
                    melhor_vizinho = g.vs["name"][w]
                    id_melhor = w
                z+=1
        #peso_da_rota+=melhor_peso
        H.append(g.vs["name"][id_melhor])
        g.delete_vertices(i)#deleta o vértice analisado do grafo e parte para o proximo a ser analisado
        i=g.vs["name"].index(melhor_vizinho)#proximo elemento a ser analisado
    H.append("0")
    print("Melhor rota:",H)
    #print("Peso da melhor rota:",peso_da_rota)
    fim = time.time()
    print("Tempo de execução:",fim - inicio,"segundos!")
    g=grafo_aux

#main
try:
    n=int(input("Quantidade de Clientes: "))+1
except:
    print("Entrada inválida")
    exit(0)
g = Graph()
g.add_vertices(n)#quantidade de vértices
for i in range(n):
    for j in range(i+1,n):#acima dig principal
        g.add_edge(i,j,weight=randint(1,1000)) #insere a aresta dado dois vertices e seu peso
g.to_directed()#tem que usar para dizer que todas arestas adicionadas são bidirecionadas
id_no=[]
for i in range(n):
    id_no.append(str(i))
g.vs["name"]=id_no #dando um "nome" para cada nó
try:
    if(int(input("Mostrar peso das arestas?[1-sim 0-não]\n->"))):
        for e in g.es(): #mostra todos os pesos por arestas
            print("Aresta: %s-%d" % (e.source, e.target))
            print("Peso %f\n" % e['weight'])
except:
    print("Entrada inválida!")
    exit(0)
while(1):
    try:
        a=int(input("[1-Força bruta 2-Vizinho mais próximo (ctrl+c)-Sair]\n-> "))
        if(a==1):
            forcaBruta()
        elif(a==2):
            VMP_Heuristica()
            break
    except:
        break
