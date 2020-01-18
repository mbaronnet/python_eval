
import numpy as np
from colorama import Fore, Style

'''
Calcul de la distance entre 2 chaines de caractères. Ici, le coût de subtiution
(cout_sub) et d'insertion (cout_ins) sont de 1 par défault mais peuvent être modifiés
'''


def red_text(text):
    '''
    Mets un texte en rouge
    '''
    return f"{Fore.RED}{text}{Style.RESET_ALL}"


def F_coeff(i, j, A: str, B: str, cout_sub, cout_ins):
    '''
    Calcul l'élément (i,j) de la matrice des scores de A et B selon
    les coûts d'une subtitution ou d'une insertion
    '''
    s = S(A, B, i, j, cout_sub)

    if i == 0:
        return j
    elif j == 0:
        return i
    else:
        return min(F_coeff(i-1, j-1, A, B, cout_sub, cout_ins) + s, F_coeff(i, j-1, A, B, cout_sub, cout_ins) + cout_ins, F_coeff(i-1, j, A, B, cout_sub, cout_ins) + cout_ins)

# Fonction pour calculer le coût de l'alignement de 2 éléments


def S(A, B, i, j, cout_sub):
    '''
    Renvoie le coût de l'alignement de 2 éléments de 2 chaines A et B
    '''
    if A[i] == B[j]:
        return 0
    else:
        return cout_sub


class Ruler:

    '''Cette classe permet de calculer la distance entre 2 chaines 
        On choisit le cout de subtitution et insertion en créant l'objet'''

    def __init__(self, A: str, B: str, cout_sub=1, cout_ins=1):
        self.A = A
        self.B = B
        self.distance = None  # Contient la distance entre les 2 chaines
        self.F = None  # Contient la matrice des scores de distance de A et B
        self.cout_sub = cout_sub
        self.cout_ins = cout_ins

    def compute(self):
        '''
        Calcule la matrice des scores des 2 chaines de l'instance de classe Ruler
        et obtient la distance correspondante
        '''

        self.F = np.array([[F_coeff(i, j, self.A, self.B, self.cout_sub, self.cout_ins)
                            for j in range(len(self.B))] for i in range(len(self.A))])
        self.distance = self.F[len(self.A)-1][len(self.B)-1]

    def report(self):
        '''
        Renvoie l'alignement correspondant à une distance minimal entre les 2 chaines. 
        Concrètement, retourne les 2 chaines modifiées (ou non) pour l'alignement.
        '''

        # On va retrouver les chemin parcouru pour arriver à la distance entre les chaines
        # Pour cela on prend le score et on regarde l'opération qui a été effectué pour l'obtenir
        F = self.F

        top = ''  # On initialise les chaines
        bottom = ''

        i = len(self.A) - 1
        j = len(self.B) - 1

        while (i, j) != (0, 0):  # Tant qu'on est pas revenu au 'premier élément' de la matrice

            score = F[i][j]  # On prend le score

            # Si le score vient du coût d'alignement des 2 derniers caractères
            # On ajoute les caractères de chacun
            if score == F[i-1][j-1] + S(self.A, self.B, i, j, self.cout_sub):

                if S(self.A, self.B, i, j, self.cout_sub) == 0:
                    top = self.A[i] + top
                    bottom = self.B[j] + bottom
                else:
                    top = red_text(self.A[i]) + top
                    bottom = red_text(self.B[j]) + bottom
                i, j = i-1, j-1

            # Si le score vient d'une insertion de la chaine A ou B,
            # On ajoute '=' pour l'un et le caractère pour l'autre

            elif score == F[i][j-1] + self.cout_ins:
                top = red_text("=") + top
                bottom = self.B[j] + bottom
                j = j-1

            elif score == F[i-1][j] + self.cout_ins:
                top = self.A[i] + top
                bottom = red_text("=") + bottom
                i = i-1

        # Si il ne reste plus qu'un caractère de chaque on les ajoute
        if (i, j) == (0, 0):

            top = self.A[i] + top
            bottom = self.B[j] + bottom

        # Si on est arrivés au bout d'une seule des chaines on rajoute des '='
        # Pour l'autre
        else:
            while i >= 0:
                top = self.A[i] + top
                bottom = red_text("=") + bottom
                i = i-1

            while j >= 0:
                top = red_text("=") + top
                bottom = self.B[j] + bottom
                j = j-1

        return(top, bottom)
