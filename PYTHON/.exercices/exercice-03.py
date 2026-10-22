nombre_a_trouver = int(input("Joueur UN: Veuillez donner un nombre entre 0 et 100 (compris)"))

if not (nombre_a_trouver >= 0 and nombre_a_trouver <= 100):
    print("Le nombre ne respecte pas les règles du jeu, fin du programme...")
else: 
    while True:
        nombre_input = int(input("Joueur DEUX: Veuillez donner un nombre entre 0 et 100 (compris)"))

        if nombre_input > nombre_a_trouver:
            print("TROP HAUT !")
        elif nombre_input < nombre_a_trouver:
            print("TROP BAS !")
        else: 
            print("FELICITATIONS, vous avez trouvé le nombre mystère !")
            break
