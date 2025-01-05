#PROJETO DE ALGORITMO II
#TRABALHO 1 
#RUBRO NEGRO

#Alunos:
#Eduardo Fernandes Albuquerque 202304940031
#Daniel Naiff da Costa 202304940010

class Node: #Nó
    def __init__(self, valor):
        self.valor = valor
        self.cor = "VERMELHO"  
        self.esquerda = None
        self.direita = None
        self.parente = None


class ArvoreRubroNegra:
    def __init__(self):
        self.NIL = Node(None)  # Nó folha vazio (NIL)
        self.NIL.cor = "PRETO"
        self.raiz = self.NIL

    def insert(self, valor):
        new_node = Node(valor)
        new_node.esquerda = self.NIL
        new_node.direita = self.NIL
        new_node.cor = "VERMELHO"

        # Inserção binária padrão
        parente = None
        atual = self.raiz
        while atual != self.NIL:
            parente = atual
            if valor < atual.valor:
                atual = atual.esquerda
            elif valor > atual.valor:
                atual = atual.direita
            else:
                print(f"Valor {valor} já está na árvore.")
                return

        new_node.parente = parente

        if parente is None:
            self.raiz = new_node  # A árvore estava vazia
        elif valor < parente.valor:
            parente.esquerda = new_node
        else:
            parente.direita = new_node

       
        self._fix_insert(new_node)

    def _fix_insert(self, node):
        while node != self.raiz and node.parente.cor == "VERMELHO":
            if node.parente == node.parente.parente.esquerda:  # Pai está à esquerda
                uncle = node.parente.parente.direita
                if uncle.cor == "VERMELHO":  # Caso 1: Tio é vermelho
                    node.parente.cor = "PRETO"
                    uncle.cor = "PRETO"
                    node.parente.parente.cor = "VERMELHO"
                    node = node.parente.parente
                else:
                    if node == node.parente.direita:  # Caso 2: Nó é filho à direita
                        node = node.parente
                        self._rotacao_esquerda(node)
                    # Caso 3: Nó é filho à esquerda
                    node.parente.cor = "PRETO"
                    node.parente.parente.cor = "VERMELHO"
                    self._rotacao_direita(node.parente.parente)
            else:  # Pai está à direita
                uncle = node.parente.parente.esquerda
                if uncle.cor == "VERMELHO":  # Caso 1: Tio é vermelho
                    node.parente.cor = "PRETO"
                    uncle.cor = "PRETO"
                    node.parente.parente.cor = "VERMELHO"
                    node = node.parente.parente
                else:
                    if node == node.parente.esquerda:  # Caso 2: Nó é filho à esquerda
                        node = node.parente
                        self._rotacao_direita(node)
                    # Caso 3: Nó é filho à direita
                    node.parente.cor = "PRETO"
                    node.parente.parente.cor = "VERMELHO"
                    self._rotacao_esquerda(node.parente.parente)

        self.raiz.cor = "PRETO"

    def _rotacao_esquerda(self, node):
        direita_child = node.direita
        node.direita = direita_child.esquerda
        if direita_child.esquerda != self.NIL:
            direita_child.esquerda.parente = node
        direita_child.parente = node.parente
        if node.parente is None:
            self.raiz = direita_child
        elif node == node.parente.esquerda:
            node.parente.esquerda = direita_child
        else:
            node.parente.direita = direita_child
        direita_child.esquerda = node
        node.parente = direita_child

    def _rotacao_direita(self, node):
        esquerda_child = node.esquerda
        node.esquerda = esquerda_child.direita
        if esquerda_child.direita != self.NIL:
            esquerda_child.direita.parente = node
        esquerda_child.parente = node.parente
        if node.parente is None:
            self.raiz = esquerda_child
        elif node == node.parente.direita:
            node.parente.direita = esquerda_child
        else:
            node.parente.esquerda = esquerda_child
        esquerda_child.direita = node
        node.parente = esquerda_child

    def pesquisar(self, valor):
        atual = self.raiz
        while atual != self.NIL and atual.valor != valor:
            if valor < atual.valor:
                atual = atual.esquerda
            else:
                atual = atual.direita
        return atual if atual != self.NIL else None

    def remover(self, valor):
        node_to_remover = self.pesquisar(valor)
        if node_to_remover is None:
            print(f"Valor {valor} não encontrado na árvore.")
            return

        self._remover_node(node_to_remover)

    def _remover_node(self, node):
        original_cor = node.cor
        if node.esquerda == self.NIL:
            temp = node.direita
            self._transplant(node, node.direita)
        elif node.direita == self.NIL:
            temp = node.esquerda
            self._transplant(node, node.esquerda)
        else:
            successor = self._minimum(node.direita)
            original_cor = successor.cor
            temp = successor.direita
            if successor.parente == node:
                temp.parente = successor
            else:
                self._transplant(successor, successor.direita)
                successor.direita = node.direita
                successor.direita.parente = successor
            self._transplant(node, successor)
            successor.esquerda = node.esquerda
            successor.esquerda.parente = successor
            successor.cor = node.cor

        if original_cor == "PRETO":
            self._fix_remover(temp)

    def _fix_remover(self, node):
        while node != self.raiz and node.cor == "PRETO":
            if node == node.parente.esquerda:
                irmao = node.parente.direita
                if irmao.cor == "VERMELHO":
                    irmao.cor = "PRETO"
                    node.parente.cor = "VERMELHO"
                    self._rotacao_esquerda(node.parente)
                    irmao = node.parente.direita
                if irmao.esquerda.cor == "PRETO" and irmao.direita.cor == "PRETO":
                    irmao.cor = "VERMELHO"
                    node = node.parente
                else:
                    if irmao.direita.cor == "PRETO":
                        irmao.esquerda.cor = "PRETO"
                        irmao.cor = "VERMELHO"
                        self._rotacao_direita(irmao)
                        irmao = node.parente.direita
                    irmao.cor = node.parente.cor
                    node.parente.cor = "PRETO"
                    irmao.direita.cor = "PRETO"
                    self._rotacao_esquerda(node.parente)
                    node = self.raiz
            else:
                irmao = node.parente.esquerda
                if irmao.cor == "VERMELHO":
                    irmao.cor = "PRETO"
                    node.parente.cor = "VERMELHO"
                    self._rotacao_direita(node.parente)
                    irmao = node.parente.esquerda
                if irmao.esquerda.cor == "PRETO" and irmao.direita.cor == "PRETO":
                    irmao.cor = "RED"
                    node = node.parente
                else:
                    if irmao.esquerda.cor == "PRETO":
                        irmao.direita.cor = "PRETO"
                        irmao.cor = "VERMELHO"
                        self._rotacao_esquerda(irmao)
                        irmao = node.parente.esquerda
                    irmao.cor = node.parente.cor
                    node.parente.cor = "PRETO"
                    irmao.esquerda.cor = "PRETO"
                    self._rotacao_direita(node.parente)
                    node = self.raiz
        node.cor = "PRETO"

    def _transplant(self, u, v):
        if u.parente is None:
            self.raiz = v
        elif u == u.parente.esquerda:
            u.parente.esquerda = v
        else:
            u.parente.direita = v
        v.parente = u.parente

    def _minimum(self, node):
        while node.esquerda != self.NIL:
            node = node.esquerda
        return node

    def display(self, node, indent="", last=True):
        if node != self.NIL:
            print(indent, end="")
            if last:
                print("D----", end="")
                indent += "     "
            else:
                print("E----", end="")
                indent += "|    "

            cor = "VERMELHO" if node.cor == "VERMELHO" else "PRETO"
            print(f"{node.valor}({cor})")
            self.display(node.esquerda, indent, False)
            self.display(node.direita, indent, True)


# Questão do slide:
rbt = ArvoreRubroNegra()
valors = [11,2,14,1,7,13,15,5,8]
for valor in valors:
    rbt.insert(valor)

print("Árvore Rubro-Negra inicial:")
rbt.display(rbt.raiz)

print("\nPesquisando valor 11:")
node = rbt.pesquisar(11)
print(f"Encontrado: {node.valor} ({node.cor})" if node else "Não encontrado")

print("\nInserindo valor 4:")
rbt.insert(4)
rbt.display(rbt.raiz)
