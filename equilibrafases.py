import numpy as npy
import math



def geraIndividuo(QUADRO: npy.array) -> npy.array:

        quadro:     npy.array = npy.zeros((len(QUADRO), 3), float)

        for circuito in range(len(QUADRO)):
            npy.random.seed()
            fase = int(npy.random.randint(0, 3, size=1))

            if QUADRO[circuito][0] == 1.0:

                quadro[circuito, fase] =  round(QUADRO[circuito,1],0)

            elif QUADRO[circuito][0] == 2.0:

                quadro[circuito, :] = round(QUADRO[circuito, 1]/2.0,0)
                quadro[circuito, fase] = 0.0

            else:

                quadro[circuito, :] = round(QUADRO[circuito][1] / 3.0,0)

        return quadro

def individuoExiste(POPULACAO:list, INDIVIDUO:npy.array)->bool:

    for i in range(len(POPULACAO)):
        for c in range(len(INDIVIDUO)):
            for f in range(len(INDIVIDUO[0])):
                if INDIVIDUO[c][f] != POPULACAO[i][c][f]:
                    return False
    return True

def geraPopulacao(NP:int, QUADRO:npy.array) -> npy.array:

        aux = npy.zeros((len(QUADRO), 3), float)
        populacao = [aux] * NP  #npy.array([aux]*len(QUADRO), float)

        for i in range(NP):
            individuo = geraIndividuo(QUADRO)
            while individuoExiste(populacao, individuo):
                    individuo = geraIndividuo(QUADRO)
            populacao[i] = individuo
        return populacao

def funcaoObjetivo(individuo:npy.array)->float:

      iA,iB,iC  = individuo.sum(0)*1.0
      In =  (math.sqrt(iA**2+iB**2+iC**2 - iA*iB-iC*(iA+iB)))
      return In

def pMelhor(POPULACAO:list)->int:
    Pmelhor:int = len(POPULACAO)+1
    melhor:float = 1e10
    aux:float = 0
    for i in range(0, len(POPULACAO)):
        aux = funcaoObjetivo(POPULACAO[i])
        if aux < melhor :
            melhor = aux
            Pmelhor = i

    return Pmelhor

def equilibraFases( POPULACAO:list, QUADRO:npy.array,  geracoes:int=500,  tol:float=1.0e-15) -> npy.array :

    posicaoMelhor:int = pMelhor(POPULACAO)
    tanQuadro: int = len(QUADRO)
    tanPop: int = len(POPULACAO)
    maxCircuitos: int = int(tanQuadro/4)
    avMelhor: float = funcaoObjetivo(POPULACAO[posicaoMelhor])
    while geracoes > 0 and avMelhor > tol:
            geracoes -= 1
            for individuo in range(0, tanPop):
                i = POPULACAO[individuo].copy()  # copia o individuo corrente para ser a base do candidato
                nc: int = (npy.random.randint(2, maxCircuitos))  # define a quantidade de circuitos que serao copiados do doador
                circuito = (npy.random.randint(0, tanQuadro, size=nc))  # escolhe o(s) circuito(s) para mutacao
                for c in circuito:  # montagem do candidato pelo cruzamento  individuo corrente-doadores e mutacao do(s) circuito(s) aleatorios no candidtado
                  # if CR > npy.random.rand():
    #cruzamento
                      indDoador = (npy.random.randint(0, tanPop))  # seleciona um doador
                      while indDoador == individuo:  # garante que o doador nao e o individuo corrente
                          indDoador = (npy.random.randint(0, tanPop))
                      i[c] = POPULACAO[indDoador][c].copy() #copia o circuito do doador no candidato

                 #  else:
    # mutacao
                      cc:int = (npy.random.randint(0, tanQuadro)) #escolhe o circuito que sera mutacionado
                      fase: int = (npy.random.randint(0, 3))  # escolhe a fase do circuito que sera mutacionado
                      if QUADRO[cc][0] == 1.0: # mutacao de circuito monofasico
                         while i[cc, fase] == 0.0:  # garante que a fase sorteada nao esta em uso
                            fase = (npy.random.randint(0, 3))
                         i[cc, :] = 0   #  desativa todas as fases
                         i[cc, fase] = round(QUADRO[cc, 1],0) # ativa  a nova fase
                      elif QUADRO[cc][0] == 2.0: #mutacao de circuito bifasico
                                while i[cc, fase] != 0.0: #garante que a fase sorteada  esta em uso
                                    fase = (npy.random.randint(0, 3))
                                i[cc, :] = round(QUADRO[cc, 1] / 2.0,0) # ativa todas a fases
                                i[cc, fase] = 0.0 # desativa a fase que estava em uso
#selecao
                avCandidato = funcaoObjetivo(i)
                avIndividuo = funcaoObjetivo(POPULACAO[individuo])
                if avCandidato < avIndividuo:
                    if avCandidato < avMelhor:
                        posicaoMelhor = individuo
                        avMelhor = avCandidato
                    POPULACAO[individuo] = i
    return POPULACAO[posicaoMelhor]


