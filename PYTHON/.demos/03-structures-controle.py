# Structure Conditionnelle

age = int(input("Quel est votre âge? "))

est_majeur = age >= 18

if est_majeur:
    print("Vous êtes majeur")
else:
    print("Vous êtes mineur")

est_majeur_usa = age >= 21
est_majeur_france = age >= 18

if est_majeur_usa:
    print("Vous êtes majeur aux USA")
elif est_majeur_france:
    print("Vous êtes majeur en France")
else:
    print("Vous êtes mineur partout...")

if est_majeur_france and not est_majeur_usa:
    print("Vous êtes majeur en France")
elif est_majeur_usa:
    print("Vous êtes majeur aux USA")
else:
    print("Vous êtes mineur partout...")


# Affectation de variable conditionnée
statut = ""
if age >= 18:
    statut = "ADULTE"
else:
    statut = "ENFANT"

# Opérateur ternaire
statut = "ADULTE" if age >= 18 else "ENFANT"
# Overkill
statut = "ADULTE AUX USA" if age >= 21 else "ADULTE EN FRANCE" if age >= 18 else "ENFANT"


choix_utilisateur = input("Choisissez une option du menu: ")

if choix_utilisateur == "1":
    print("Vous avez choisi un Coca Cola")
elif choix_utilisateur == "2":
    print("Vous avez choisi un Sprite")
elif choix_utilisateur == "3":
    print("Vous avez choisi un Ice Tea")
elif choix_utilisateur == "4":
    print("Vous avez choisi une Volvic")
elif choix_utilisateur == "5":
    print("Vous avez choisi un Orangina")
else:
    print("Je n'ai pas compris votre choix, veuillez indiquer une valeur entre 1 et 5 compris")


match choix_utilisateur:
    case "1":
        print("Vous avez choisi un Coca Cola")
        print("Merci pour votre achat !")
    case "2":
        print("Vous avez choisi un Sprite")
        print("Merci pour votre achat !")
    case "3":
        print("Vous avez choisi un Ice Tea")
        print("Merci pour votre achat !")
    case "4":
        print("Vous avez choisi une Volvic")
        print("Merci pour votre achat !")
    case "5":
        print("Vous avez choisi un Orangina")
        print("Merci pour votre achat !")
    case _:
        print("Je n'ai pas compris votre choix, veuillez indiquer une valeur entre 1 et 5 compris")

## Structure itératives

age = 21
# age = int(input("Quel est votre âge ? "))

while age < 18:
    print("Je suis mineur...")
    age = age + 1
else:
    print("Je ne boucle pas...")

print("Je suis désormais majeur !")


# Boucle permettant de demander une saisie spécifique pour sortir de la boucle
entre_utilisateur = ""

while entre_utilisateur != "STOP":
    entre_utilisateur = input("Tapez 'STOP' pour sortir de la boucle... ")


# Réalise manuellement une boucle infinie avec sortie via instruction 'break'
while True:
    if input("Tapez 'STOP' pour sortir de la boucle... ") == "STOP":
        break # Casse la boucle manuellement


# Boucle avec X itération grâce à un générateur de nombres entiers
for i in range(5):
    print(str(i) + ": Je me répète...")