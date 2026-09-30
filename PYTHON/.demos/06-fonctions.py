def dire_bonjour():
    print("Hello world!")


print("Hello world!")
dire_bonjour()


ensemble_nombre_a = [1, 47, 25, 48, 84]

def faire_la_somme(ensemble):
    somme = 0
    for n in ensemble:
        somme += n

    print(f"La somme de l'ensemble {ensemble} est : {somme}")

faire_la_somme(ensemble_nombre_a)

ensemble_nombre_b = [15, 84, 96, 25, 88]

faire_la_somme(ensemble_nombre_b)


def donne_la_somme(ensemble):
    somme = 0
    for n in ensemble:
        somme += n

    return somme

resultat_de_la_somme_des_deux_ensembles = donne_la_somme(ensemble_nombre_a) + donne_la_somme(ensemble_nombre_b)


def nombre_max(nombre_a = 0, nombre_b = 0):
    if nombre_a >= nombre_b:
        return nombre_a
    
    # else:
    #     return nombre_b
    
    return nombre_b
    

print(f"Le plus grand nombre entre 147 et 2548 est: {nombre_max(147, 2548)}")

print(nombre_max(nombre_b=14))

from utils import addition

la_somme = addition(25, 47)