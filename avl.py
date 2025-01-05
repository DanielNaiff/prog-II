#PROJETO DE ALGORITMO II
#TRABALHO 1 
#AVL

#Alunos:
#Eduardo Fernandes Albuquerque 202304940031
#Daniel Naiff da Costa 202304940010

class No:
    def __init__(self, valor):
        self.valor = valor
        self.direita = None
        self.esquerda = None
        self.altura = 0

class Cores:
    RESET = "\033[0m"
    VERDE = "\033[32m"
    VERMELHO = "\033[31m"
    AMARELO = "\033[33m"
    AZUL = "\033[34m"

def maior(a, b):
    return a if a > b else b

def altura_do_no(no):
    if no is None:
        return -1
    return no.altura

def fator_de_balanceamento(no):
    if no is None:
        return 0
    return altura_do_no(no.esquerda) - altura_do_no(no.direita)

def rotacao_esquerda(raiz):
    y = raiz.direita
    filho = y.esquerda
    y.esquerda = raiz
    raiz.direita = filho
    raiz.altura = maior(altura_do_no(raiz.esquerda), altura_do_no(raiz.direita)) + 1
    y.altura = maior(altura_do_no(y.esquerda), altura_do_no(y.direita)) + 1
    return y

def rotacao_direita(raiz):
    y = raiz.esquerda
    filho = y.direita
    y.direita = raiz
    raiz.esquerda = filho
    raiz.altura = maior(altura_do_no(raiz.esquerda), altura_do_no(raiz.direita)) + 1
    y.altura = maior(altura_do_no(y.esquerda), altura_do_no(y.direita)) + 1
    return y

def rotacao_direita_esquerda(raiz):
    raiz.direita = rotacao_direita(raiz.direita)
    return rotacao_esquerda(raiz)

def rotacao_esquerda_direita(raiz):
    raiz.esquerda = rotacao_esquerda(raiz.esquerda)
    return rotacao_direita(raiz)

def balancear(raiz):
    fb = fator_de_balanceamento(raiz)
    
    if fb < -1 and fator_de_balanceamento(raiz.direita) <= 0:
        return rotacao_esquerda(raiz)
    elif fb > 1 and fator_de_balanceamento(raiz.esquerda) >= 0:
        return rotacao_direita(raiz)
    elif fb > 1 and fator_de_balanceamento(raiz.esquerda) < 0:
        return rotacao_esquerda_direita(raiz)
    elif fb < -1 and fator_de_balanceamento(raiz.direita) > 0:
        return rotacao_direita_esquerda(raiz)
    return raiz

def inserir(raiz, valor):
    if raiz is None:
        return No(valor)

    if valor < raiz.valor:
        raiz.esquerda = inserir(raiz.esquerda, valor)
    elif valor > raiz.valor:
        raiz.direita = inserir(raiz.direita, valor)
    else:
        print(f"{Cores.VERMELHO}Inserção não realizada!{Cores.RESET}")
        return raiz

    raiz.altura = maior(altura_do_no(raiz.esquerda), altura_do_no(raiz.direita)) + 1
    raiz = balancear(raiz)
    return raiz

def remover(raiz, chave):
    if raiz is None:
        print(f"{Cores.VERMELHO}Valor não encontrado{Cores.RESET}")
        return None

    if chave == raiz.valor:
        if raiz.esquerda is None and raiz.direita is None:
            print(f"{Cores.AMARELO}Elemento folha removido: {chave}{Cores.RESET}")
            return None
        elif raiz.esquerda is not None and raiz.direita is not None:
            aux = raiz.esquerda
            while aux.direita is not None:
                aux = aux.direita
            raiz.valor = aux.valor
            aux.valor = chave
            print(f"{Cores.AMARELO}Elemento trocado: {chave}{Cores.RESET}")
            raiz.esquerda = remover(raiz.esquerda, chave)
            return raiz
        else:
            aux = raiz.esquerda if raiz.esquerda is not None else raiz.direita
            print(f"{Cores.AMARELO}Elemento com 1 filho removido: {chave}{Cores.RESET}")
            return aux

    if chave < raiz.valor:
        raiz.esquerda = remover(raiz.esquerda, chave)
    else:
        raiz.direita = remover(raiz.direita, chave)

    raiz.altura = maior(altura_do_no(raiz.esquerda), altura_do_no(raiz.direita)) + 1
    raiz = balancear(raiz)
    return raiz

def pesquisar(raiz, valor):
    if raiz is None:
        print(f"{Cores.VERMELHO}Valor não encontrado!{Cores.RESET}")
        return None
    if valor == raiz.valor:
        print(f"{Cores.AZUL}Valor {valor} encontrado!{Cores.RESET}")
        return raiz
    elif valor < raiz.valor:
        return pesquisar(raiz.esquerda, valor)
    else:
        return pesquisar(raiz.direita, valor)

def imprimir(raiz, nivel=0):
    if raiz:
        imprimir(raiz.direita, nivel + 1)
        print("\n" + "\t" * nivel + f"{Cores.AZUL}{raiz.valor}{Cores.RESET}")
        imprimir(raiz.esquerda, nivel + 1)

def menu():
    raiz = None
    while True:
        print(f"\n\n\t{Cores.VERDE}1 - Inserir{Cores.RESET}")
        print(f"\t{Cores.VERDE}2 - Remover{Cores.RESET}")
        print(f"\t{Cores.VERDE}3 - Imprimir (A árvore será representada 'deitada' da esquerda para a direita){Cores.RESET}")
        print(f"\t{Cores.VERDE}4 - Pesquisar{Cores.RESET}")
        print(f"\t{Cores.VERDE}5 - Sair{Cores.RESET}")

        opcao = int(input(f"{Cores.AMARELO}Escolha uma opção: {Cores.RESET}"))

        if opcao == 1:
            valor = int(input(f"{Cores.AMARELO}Digite o valor a ser inserido: {Cores.RESET}"))
            raiz = inserir(raiz, valor)
        elif opcao == 2:
            valor = int(input(f"{Cores.AMARELO}Digite o valor a ser removido: {Cores.RESET}"))
            raiz = remover(raiz, valor)
        elif opcao == 3:
            imprimir(raiz)
        elif opcao == 4:
            valor = int(input(f"{Cores.AMARELO}Digite o valor a ser pesquisado: {Cores.RESET}"))
            pesquisar(raiz, valor)
        elif opcao == 5:
            print(f"{Cores.VERMELHO}Programa finalizado{Cores.RESET}")
            break
        else:
            print(f"{Cores.VERMELHO}\nOpção inválida!{Cores.RESET}")


if __name__ == "__main__":
    menu()
