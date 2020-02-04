import random
import os
from time import sleep

class Jogador:
    
    def __init__(self, nome):
        self.nome = nome
        self.deck = []
        self.proxJogador = None
        self.anteriorJogador = None

    def setProxJogador(self, prox):
        self.proxJogador = prox
    
    def getProxJogador(self):
        return self.proxJogador
    
    def setAnteriorJogador(self, anterior):
        self.anteriorJogador = anterior

    def getAnteriorJogador(self):
        return self.anteriorJogador

    def getNome(self):
        return  self.nome

class Jogo:

    def __init__(self, nJogadores):
        self.stack = []
        self.discardStack = []
        self.nJogadores = nJogadores
        self.inicioFila = None
        self.fimFila = None
        self.auxJogador = None
        self.fimJogo = False
        self.round = 0
    
    def stackGen(self):
        arquivo = open('/home/nityananda/Transferências/EstudoPython/Uno/cartas.txt','r')
        for i in arquivo:
            i = i.split(',')
            for j in i:
                if j== "\n":
                    pass
                else:
                    self.stack.append(j)
        arquivo.close()
    
    def deckGen(self):
        aux = self.inicioFila
        for i in range(self.nJogadores):
            for j in range(7):
                x = random.choice(self.stack)
                aux.deck.append(x)
                self.stack.remove(x)
                aux = aux.getProxJogador()
        #self.imprimirFilaJogadores()
    
    def deckPrint(self):
        count1 = 0
        count2 = len(self.auxJogador.deck)*3
        for i in self.auxJogador.deck:
            for j in i:
                count1 += 1
        count1 += count2
        print("-"*count1)
        saida =''
        for i in self.auxJogador.deck:
            saida += "|" + str(i) + " "
        saida += "|"
        print(saida)
        print("-"*count1)

    def filaJogadores(self, numPlayers):
        for i in range(numPlayers):
            if(i == 0):
                nome = str(input("Insira seu nome : "))
                novoJogador = Jogador(nome)
                self.inicioFila = novoJogador
                self.fimFila = novoJogador
            else:
                novoJogador = Jogador(str(i + 1))
                if(i != numPlayers - 1):
                    self.fimFila.setProxJogador(novoJogador)
                    novoJogador.setAnteriorJogador(self.fimFila)
                    self.fimFila = novoJogador
                else:
                    self.fimFila.setProxJogador(novoJogador)
                    novoJogador.setAnteriorJogador(self.fimFila)
                    self.fimFila = novoJogador
                    self.fimFila.setProxJogador(self.inicioFila)
                    self.inicioFila.setAnteriorJogador(self.fimFila)

    def imprimirFilaJogadores(self):
        noAux = self.inicioFila
        noAux2 = self.fimFila
        saida = ''
        saida2 = ''
        for i in range(self.nJogadores):
            saida += str(noAux.getNome()) + " / "
            print(noAux.nome)
            print(noAux.deck)
            noAux = noAux.getProxJogador()
        #for i in range(self.nJogadores):
        #    saida2 += str(noAux2.getNome()) + " / "
        #    noAux2 = noAux2.getAnteriorJogador()

    def checkEndGame(self):
        noAux = self.inicioFila
        for i in range(self.nJogadores):
            if(len(noAux.deck) == 0):
                print("O "+ str(noAux.nome) + "e o ganhador !!")
                self.fimJogo = True
                return True
            else:
                noAux = noAux.getProxJogador()
        return False
    
    def discarte(self):
        sleep(1); os.system('clear')
        print("Vez do jogador : " + str(self.auxJogador.nome))
        self.deckPrint()
        if(self.round == 0):
            pass
        else:
            pass
    def rodadas(self):
        self.auxJogador = self.inicioFila
        if(Jogo.checkEndGame(self) == False):
            self.discarte()


    def partida(self):
        self.filaJogadores(self.nJogadores)
        self.stackGen()
        self.deckGen()
        self.rodadas()


njogadores = int(input("Quantos jogadores irao jogar ?\nObs: Min: 2 jogadores.\nMax: 10 jogadores.\n"))
while(njogadores<2 or njogadores>10):
    njogadores = int(input("Quantos jogadores irao jogar ?\nObs: Min: 2 jogadores.\nMax: 10 jogadores.\n"))

Partida = Jogo(njogadores)
Partida.partida()