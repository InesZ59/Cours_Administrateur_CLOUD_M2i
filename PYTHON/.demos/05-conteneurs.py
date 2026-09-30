## LIST
mon_nombre = 123

mes_nombres = [1, 2, 3, 4, 5]
mes_nombres = list(1, 2, 3, 4, 5)
mes_nombres_virgules = [1.23, 4.84, 12.14]
mes_mots = ["Toto", "Tata", "Pomme", "Chien"]
mes_booleens = [True, False, True, True]
mes_elements = [12, "Tata", True, [12, 14]]

mon_deuxieme_nombre = mes_nombres[1]
mes_nombres_du_2e_au_4e = mes_nombres[1:3]

la_date = "DD/MM/YYYY"
la_date_ensemble = la_date.split('/') # ['DD', 'MM', 'YYYY']
jour, moi, annee = la_date_ensemble

premier, deuxieme, troisieme, *reste = mes_nombres # 1 | 2 | 3 | [4, 5]

ma_liste_vide = []
ma_liste_vide_bis = list()

ma_liste_vide.append("Toto") # [] => ["Toto"]

# ["Toto"] => ["Toto", "Tata", "Tutu"]
ma_liste_vide.extend(["Tata", "Tutu"])

# ERROR: ["Toto"] => ["Toto", ["Tata", "Tutu"]]
ma_liste_vide.append(["Tata", "Tutu"])

# ["Toto", "Tata", "Tutu"] => ["Toto", "Tata"]
element_retire = ma_liste_vide.pop()

# ["Toto", "Tata", "Tutu"] => ["Toto", "Tutu"]
ma_liste_vide.remove("Tata")

# ["Toto", "Tata", "Tutu"] => ["Toto", "Truc", "Tata", "Tutu"]
ma_liste_vide.insert(1, "Truc")

ma_liste_vide.count("Toto") # 1 seul Toto dans la liste

len(ma_liste_vide) # 3 si la liste vaut ["Toto", "Tata", "Tutu"]

for element in mes_nombres:
    print(element)

mes_nombres_de_0_a_9 = list(range(10))
mes_nombres_de_0_a_9.append(10)
mes_nombres_de_0_a_10 = list(mes_nombres_de_0_a_9)

mes_nombres_de_0_a_10 = list(range(11))
mes_nombres_de_0_a_10 = [range(11)]

mes_nombres_pairs = []

for nombre in range(11):
    if nombre % 2 == 0:
        mes_nombres_pairs.append(nombre)

print(mes_nombres_pairs) # [0, 2, 4, 6, 8, 10]

# for nombre in range(11):
#     if nombre % 2 == 0:
#         mes_nombres_pairs_carres.append(nombre ** 2)

mes_nombres_pairs_carre = [nombre ** 2 for nombre in range(11) if nombre % 2 == 0]

## TUPLE

mes_nombres = (1, 2, 3, 4, 5)
mes_nombres = tuple(1, 2, 3, 4, 5)

for nombre in mes_nombres:
    print(nombre)

mes_nombres.count(2) # Combien de fois j'ai '2' dans mon ensemble

premier, deuxieme, *reste = mes_nombres

## SET

mes_nombres = {1, 2, 3, 4, 5}
mes_nombres = set(1, 2, 3, 4, 5)

mes_fruits_liste = ["Pomme", "Mangue", "Banane", "Mangue", "Banane", "Pomme", "Pomme"]
nb_elements_liste_fruits = len(mes_fruits_liste)

somme = 0
mes_fruits_deja_comptabilise = []

# for fruit in mes_fruits_liste:
#     if fruit not in mes_fruits_deja_comptabilise:
#         mes_fruits_deja_comptabilise.append(fruit)
#         somme += 1

mes_fruits_liste_sans_duplicats = set(mes_fruits_liste)
len(mes_fruits_liste_sans_duplicats)

# Ne va rien provoquer car on ne peut pas avoir de duplicats dans un set
mes_nombres.add(4)

## Dictionnaire

carnet_adresse = {
    "Elliot": "5, Rue des Fleurs", 
    "John": "27, Chemin de Fer"
}

print(f"Adresse d'Elliot: {carnet_adresse['Elliot']}")

carnet_adresse['Lola'] = "14, Avenue des Champs"

nouvelle_personne = input("Quel est le nom de la personne")

carnet_adresse[nouvelle_personne] = input(f"Veuillez donner l'adresse de '{nouvelle_personne}': ")

for prenom in carnet_adresse.keys():
    print(prenom)

for adresse in carnet_adresse.values():
    print(adresse)

for key, value in carnet_adresse.items():
    print(f"{key}: {value}")

liste_nombre_pairs = [nombre for nombre in range(101) if nombre % 2 == 0]
liste_nombre_pairs_carre = [nombre ** 2 for nombre in range(101) if nombre % 2 == 0]

dictionnaire_nombres_et_carre = {nombre: nombre ** 2 for nombre in range(101) if nombre % 2 == 0}