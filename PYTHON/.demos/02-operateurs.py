nombre_un = 5
nombre_deux = 10
nombre_trois = 4

## Les Opérateurs Arithmétiques
la_somme = 5 + 10 # 15
la_somme_variables = nombre_un + nombre_deux

la_concatenation = "5" + "10" # "510"

la_difference = nombre_un - nombre_deux # -5

le_quotient = nombre_deux / nombre_trois # 2.5

le_quotient_euclidien = nombre_deux // nombre_trois # 2

le_reste = nombre_deux % nombre_trois # 2

le_produit = nombre_un * nombre_trois # 20

la_multiplication_texte = "ABC" * 3 # "ABCABCABC" 

# La caractère espace, pour un ordinateur => \0

la_puissance = nombre_deux ** nombre_un # 100.000

## Les Opérateurs de comparaison 
egalite = 10 == 11 # False

difference = 10 != 11 # True

superiorite = 10 > 5 # True

superiorite_ou_egalite = 10 >= 5 # True

inferiorite = 10 < 5 # False

inferiorite_ou_egalite = 10 <= 10 # True

## Les Opérateurs Logique
possede_carte_bibliotheque = True
argent = 25
age = int(input("Quel est votre âge ? ")) # 'Casting' en Integer pour le traiter en tant que nombre entier

acces_bibliotheque = age >= 12 and possede_carte_bibliotheque

acces_avec_paiement_possible_2_euros = argent >= 2 or possede_carte_bibliotheque

est_mineur = not (age >= 18)

age_entre_10_et_18_compris = age >= 10 and age <= 18
age_entre_10_et_18_compris = 10 <= age <= 18