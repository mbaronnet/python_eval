' Codage de Huffman pour compresser des données textuelles '


def occur(text):
    '''
    Renvoie le nombre d'occurences de chaque caractères 
    d'un texte sous forme de dictionnaire 
    '''

    table_occur = {}
    for el in text:
        if el in list(table_occur.keys()):
            table_occur[el] = table_occur[el] + 1
        else:
            table_occur[el] = 1
    return table_occur


class Node:
    '''
    Classe noeud qui représente le noeud de l'arbre de Huffman : 
    Un noeud a un type de caractère et son poids et ses noeuds fils 
    droite et gauche associés 
    '''

    def __init__(self, caract: str, weight,  right=None, left=None):
        self.caract = caract
        self.weight = weight
        self.right = right
        self.left = left

    def __repr__(self):
        return(f'{self.caract} : {self.weight}')


class TreeBuilder:

    '''
    Classe permettant de construire l'arbre de Huffman associé à un texte 
    '''

    def __init__(self, text: str):

        self.text = text

    def tree(self):
        '''
        La méthode tree construit l'arbre : elle retourne le noeud racine 
        qui contient toutes les informations sur l'arbre 
        '''

        # On construit une pile triée avec les noeuds "feuilles de l'arbre"
        # C'est à dire les caractères et leur occurences

        pile = [Node(lettre, occ)
                for (lettre, occ) in occur(self.text).items()]
        pile = sorted(pile, key=lambda x: x.weight)

        # Tant que la pile n'est pas réduite à un élément, on enlève les deux noeuds de
        # plus petits poids de la pile et on les "fusionnent" en additionant leur poids
        # en un nouveau noeud que l'on place dans la pile

        while len(pile) > 1:

            # On récupère les noeuds de plus petit poids
            node_1, node_2 = pile[0], pile[1]

            del pile[0]
            del pile[0]

            # Création du nouveau noeud
            new_node = Node(node_1.caract + node_2.caract,
                            node_1.weight + node_2.weight, right=node_1, left=node_2)

            # Mise à jour de la pile
            pile = [new_node] + pile
            pile = sorted(pile, key=lambda x: x.weight)

        return(pile[0])


def dico_code(tree: Node, text: str):
    '''
    Renvoie un dictionnaire qui à chaque caracètre fait correspondre
    son caracère "codé" de Huffman
    '''

    node = tree
    code_caract = ''
    codage = {}

    # Pour chaque caractère dans le texte, si le caractère n'est pas déjà recensé,
    for caract in text:

        if caract not in list(codage.keys()):

            # On créé son code en partant de la racine est en ajoutant 1 (gauche) ou 0
            # Jusqu'à ce qu'on arrive à sa feuille.

            while node.caract != caract:
                if caract in node.right.caract:
                    code_caract = code_caract + '0'
                    node = node.right

                elif caract in node.left.caract:
                    code_caract = code_caract + '1'
                    node = node.left

            # On recense le caractère avec son code associé
            codage[caract] = code_caract
            code_caract = ''
            node = tree  # On repart à la racine

    return(codage)


class Codec:

    '''
    Classe permettant de coder un texte dont on a construit l'arbre de Huffman 
    précédemment
    '''

    def __init__(self, tree: Node):

        self.tree = tree

    def encode(self, text: str):
        '''
        Renvoie le code de Huffman du texte correspondant
        '''

        # On récupère le dictionnaire qui associe à chaque caractère son code de Huffman
        self.code = dico_code(self.tree, text)
        code = ''

        # On remplace chaque caractère par son code correspondant dans le texte
        for caract in text:

            code = code + self.code[caract]

        return(code)

    def decode(self, encoded: str):
        '''
        Renvoie le texte correspondant à un codage de Huffman binaire 
        '''

        # On se place à la racine de l'arbre
        caract = self.tree.caract
        node = self.tree
        text = ''

        # Tant qu'on a pas parcouru tout le texte, on descends en suivant les
        # 0 et 1 du code correspondant à droite ou gauche. A chaque fois qu'on
        # arrive à une feuille, on ajoute le caractère et on remonte à la
        # racine de l'arbre.

        while len(encoded) > 0:

            # Tant qu'on a pas un unique caractère on suit le chemin du code
            while len(caract) > 1 and len(encoded) > 0:

                if encoded[0] == '1':
                    node = node.left
                elif encoded[0] == '0':
                    node = node.right

                caract = node.caract
                encoded = encoded[1:]

            # Arrivée à une feuille : ajout du caractère et remontée à la racine
            text = text + node.caract
            node = self.tree
            caract = node.caract

        return(text)
