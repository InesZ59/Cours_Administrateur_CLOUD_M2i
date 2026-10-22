from datetime import date

nom = input("Veuillez entrer votre NOM: ")

prenom = input("Veuillez entrer votre PRENOM: ")

date_actuelle = date.today()

date_naissance_input = input("Veuillez donner votre date de naissance (au format DD/MM/YYYY): ")
# ensemble = date_naissance_input.split('/')
# jour, mois, annee = ensemble
jour, mois, annee = date_naissance_input.split('/')
date_naissance = date(int(annee), int(mois), int(jour))

age = date_actuelle.year - date_naissance.year

# Méthode classique
if date_actuelle.month < date_naissance.month:
    age = age - 1
    # age -= 1
elif date_actuelle.month == date_naissance.month and date_actuelle.day < date_naissance.day:
    age -= 1

# # Méthode Tuple
# if (date_actuelle.month, date_actuelle.day) < (date_naissance.month, date_naissance.day):
#     age -= 1

# Bonjour [prenom] [nom], vous avez [age] ans!

# message_perso_f_string = f"Bonjour {prenom} {nom}, vous avez {age} ans!"
message_perso = "Bonjour " + prenom + " " + nom + ", vous avez " + str(age) + " ans!"
print(message_perso)