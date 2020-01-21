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
    
    def stackGen(self):
        arquivo = open('cartas.txt','r')
        for i in arquivo:
            i = i.split(',')
            for j in i:
                if j== "\n":
                    pass
                else:
                    self.stack.append(j)
        arquivo.close()
        print(self.stack)

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
        self.imprimir()

    def imprimir(self):
        noAux = self.inicioFila
        noAux2 = self.fimFila
        saida = ''
        saida2 = ''
        for i in range(self.nJogadores):
            saida += str(noAux.getNome()) + " / "
            noAux = noAux.getProxJogador()
        for i in range(self.nJogadores):
            saida2 += str(noAux2.getNome()) + " / "
            noAux2 = noAux2.getAnteriorJogador()
        print(saida)
        print()
        print(saida2)


    def partida(self):
        self.filaJogadores(self.nJogadores)
        self.stackGen()


njogadores = int(input("Quantos jogadores irao jogar ?\nObs: Min: 2 jogadores.\nMax: 10 jogadores.\n"))
while(njogadores<2 or njogadores>10):
    njogadores = int(input("Quantos jogadores irao jogar ?\nObs: Min: 2 jogadores.\nMax: 10 jogadores.\n"))

Partida = Jogo(njogadores)
Partida.partida()