import os
# On se place dans le bon fichier
os.chdir('c:\\Users\\Maelle\\Documents\\Cours\\info\\eval\\needleman_wunsch')
import ruler as r  # On importe le module ruler



with open('DATASET.txt') as f:

    ftab = f.read().splitlines()  # On prend une liste des lignes du fichier

    n = 0  # Numérote les exemples
    n_current_line = 0
    current_line = []  # Stock temporairement les lignes

    for line in ftab:

        # On récupère par 2 les lignes dans current_line
        n_current_line = n_current_line + 1
        current_line.append(line.strip())

        if n_current_line == 2:

            n = n + 1
            # On créé la classe pour calculer la distance et on imprime les alignements
            ruler = r.Ruler(current_line[0], current_line[1])
            ruler.compute()

            print(f"====== example # {n} - distance = {ruler.distance}")

            top, bottom = ruler.report()
            print(top)
            print(bottom)

            current_line = []
            n_current_line = 0
