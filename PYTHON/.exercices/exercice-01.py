nom = input("Veuillez entrer votre NOM: ")

prenom = input("Veuillez entrer votre PRENOM: ")

# age = int(input("Veuillez entrer votre AGE: "))
age_str = input("Veuillez entrer votre AGE: ")
# age = int(age_str)


# Bonjour [prenom] [nom], vous avez [age] ans!
message_perso = "Bonjour " + prenom + " " + nom + ", vous avez " + age_str + " ans!"
print(message_perso)