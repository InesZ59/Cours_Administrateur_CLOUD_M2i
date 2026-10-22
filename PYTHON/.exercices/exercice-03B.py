from random import randint

nombre_a_trouver_a = randint(0, 100)
nombre_a_trouver_b = randint(0, 100)

while nombre_a_trouver_a == nombre_a_trouver_b:
    nombre_a_trouver_b = randint(0, 100)

cibles = {
    "Joueur A": nombre_a_trouver_a,
    "Joueur B": nombre_a_trouver_b
}

statut_gagnant = {
    "Joueur A": False,
    "Joueur B": False
}

essais = {
    "Joueur A": 0,
    "Joueur B": 0
}

tour = 0

# while not statut_gagnant['Joueur A'] and not statut_gagnant['Joueur B']:
while not all(statut_gagnant):
    # Alternance entre les clés 'Joueur A' et 'Joueur B'
    joueur_actuel = list(cibles)[tour % 2]

    # Si le joueur actuel a déjà gagné, on passe la main au joueur suivant
    if statut_gagnant[joueur_actuel]:
        tour += 1
        continue

    # On demande le nombre au joueur courant
    nombre_input = int(input(f"{joueur_actuel}: Veuillez donner un nombre entre 0 et 100 (compris)"))
    
    # On incrémente le nombre d'essais du joueur courant
    essais[joueur_actuel] += 1

    # On récupère le nombre à trouver du joueur courant
    nombre_a_trouver_pour_joueur_actuel = cibles[joueur_actuel]

    # Logique du jeu du nombre mystère pour le joueur courant
    if nombre_input > nombre_a_trouver_pour_joueur_actuel:
        print("TROP HAUT !")
    elif nombre_input < nombre_a_trouver_pour_joueur_actuel:
        print("TROP BAS !")
    else: 
        print(f"FELICITATIONS, vous avez trouvé le nombre mystère en {essais[joueur_actuel]} essais !")
        statut_gagnant[joueur_actuel] = True # S'il a gagné, on passe son statut à 'Gagné' => True

    tour += 1

nb_essais_joueur_a = essais["Joueur A"]
nb_essais_joueur_b = essais["Joueur B"]


# On compare le nombre d'essais des deux joueurs pour déclarer le vainqueur
if nb_essais_joueur_a == nb_essais_joueur_b:
    print("Egalité des deux joueurs !")
elif nb_essais_joueur_a > nb_essais_joueur_b:
    print("Le joueur B à gagné !")
else:
    print("Le joueur A à gagné !")


