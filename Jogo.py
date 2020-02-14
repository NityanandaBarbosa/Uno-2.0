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
        self.pegarCard = 0
        self.sentidoReverso = False
        self.acumuloCartas = 0
        self.enqMais = False
        self.ultimoDiscarte = [] 
    
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
    
    def deckPrint(self, thing):
        count1 = 0
        count2 = (len(thing)-1)*3
        for i in thing:
            for j in i:
                count1 += 1
        count1 += count2 + 4
        print("-"*count1)
        saida =''
        for i in thing:
            saida += "| " + str(i) + " "
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
                print("O "+ str(noAux.nome) + " e o ganhador !!")
                self.fimJogo = True
                return True
            else:
                noAux = noAux.getProxJogador()
        return False
    
    def pegarCarta(self):
        novaCarta = ''
        if(self.pegarCard == 0):
            if(len(self.stack) != 0):
                novaCarta = random.choice(self.stack)
                self.stack.remove(novaCarta)
            else:
                novaCarta = random.choice(self.discardStack)
                self.discardStack.remove(novaCarta)
            self.auxJogador.deck.append(novaCarta)
        self.pegarCard += 1

    def reversoEblockCheck(self,escolhaCheck):
        if(escolhaCheck[1] == 'reverso'):
            self.sentidoReverso = True
        else:
            if(escolhaCheck[1] == 'cancela'):
                self.proxJogar()
    
    def maisCarta(self, escolhaCheck):
        if(self.enqMais == False):
            if(escolhaCheck[1] in ['+2','+4']):
                self.enqMais = True
                self.acumuloCartas += int(escolhaCheck[1])
        else:
            if(escolhaCheck[1] in ['+2','+4']):
                self.acumuloCartas += int(escolhaCheck[1])
                print("Acumulado de cartas está no total de : " + str(self.acumuloCartas))
            else:
                if(len(self.stack) != 0):
                    for i in range(self.acumuloCartas):
                        novaCarta = random.choice(self.stack)
                        self.auxJogador.deck.append(novaCarta)
                        self.stack.remove(novaCarta)
                else:
                   for i in range(self.acumuloCartas):
                        novaCarta = random.choice(self.discardStack)
                        self.auxJogador.deck.append(novaCarta)
                        self.discardStack.remove(novaCarta) 
                print("Voce receberá : " + str(self.acumuloCartas))
                self.deckPrint(self.auxJogador.deck)
                self.enqMais = False; self.acumuloCartas = 0


    def discarteCheck(self, escolha,escolhaCheck,confirm):
        if(escolha == 0):
            self.pegarCarta()
            print("Foi pego uma carta, caso não seja possivel discarte aperte 0 novamente")
            self.deckPrint(self.auxJogador.deck)
            if(self.pegarCard == 2):
                confirm = True
                if(self.enqMais == True):
                    for i in range(self.acumuloCartas):
                        self.pegarCarta()
                    print("Voce receberá : " + str(self.acumuloCartas))
                    self.deckPrint(self.auxJogador.deck)
                    self.enqMais = False; self.acumuloCartas = 0
        else:
            if(escolhaCheck[0] == self.ultimoDiscarte[0]):
                self.reversoEblockCheck(escolhaCheck)
                self.maisCarta(escolhaCheck)
                confirm = True
            elif(escolhaCheck[1] == self.ultimoDiscarte[1]):
                if(escolhaCheck[0] != self.ultimoDiscarte[1]):
                    print("Cor foi mudada para : " + str(escolhaCheck[0]))
                self.maisCarta(escolhaCheck)
                confirm = True
            else:
                if(escolhaCheck[0] == 'coringa'):
                    cores = ['vermelho','azul','verde','amarelo']; cor = 0
                    self.deckPrint(cores)
                    while(cor > 4 or cor < 1):
                        cor = int(input("Escolha a cor :"))
                    print("Cor foi mudada para : " + str(cores[cor-1]))
                    escolhaCheck[0] = cores[cor-1]
                    self.maisCarta(escolhaCheck)
                    confirm = True
                #elif(escolhaCheck[1] in ['+2','+4']):
                #    self.maisCarta(escolhaCheck)
                #    confirm = True
        return confirm,escolhaCheck
    
    def discarte(self):
        sleep(1); 
        #os.system('clear'); 
        escolha = 99; confirme = False;
        print("Vez do jogador : " + str(self.auxJogador.nome)+ "\nCarta passada : "+ str(self.ultimoDiscarte))
        self.deckPrint(self.auxJogador.deck)
        if(self.round == 0):
            print('Pode jogar qualquer carta.\nObs:Cartas de efeito não funcionaram.')
            while(escolha > len(self.auxJogador.deck)):
                escolha = int(input("Escolha a carta a ser jogada"))
            escolha = self.auxJogador.deck[escolha - 1]
            self.ultimoDiscarte = escolha.split(' ')
            self.auxJogador.deck.remove(escolha)
            confirme = True
            print(self.auxJogador.deck, self.ultimoDiscarte)
        else:
            while(confirme == False):
                if(self.enqMais == True):
                    print("Mais cartas acumulada total de cartas : " + str(self.acumuloCartas))
                escolha = int(input("Escolha a carta a ser jogada")) 
                if(escolha <= len(self.auxJogador.deck) and escolha >= 0):
                    escolhaCheck = self.auxJogador.deck[escolha - 1].split(' ')
                    print(escolhaCheck)
                    confirme,escolhaCheck = self.discarteCheck(escolha,escolhaCheck,confirme)
                    if(confirme == True):
                        if(self.pegarCard == 2):
                            print("Passa jogada !!")
                        else:
                            del self.auxJogador.deck[escolha - 1]
                            self.ultimoDiscarte = escolhaCheck
                        print(self.auxJogador.deck, self.ultimoDiscarte)
                        self.pegarCard = 0
                else:
                    print("Jogada Invalida, será necessario tentar jogar outra carta")
            print("sai do while " + str(confirme))
        self.round += 1 
        self.proxJogar()
        print()

    def rodadas(self):
        self.auxJogador = self.inicioFila
        while(Jogo.checkEndGame(self) == False):
            self.discarte()

    
    def proxJogar(self):
        if(self.sentidoReverso == True):
            self.auxJogador = self.auxJogador.getAnteriorJogador()
        else:
            self.auxJogador = self.auxJogador.getProxJogador()

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