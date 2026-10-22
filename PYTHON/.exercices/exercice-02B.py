menu = {
    "1": ("Coca Cola", 1.80),
    "2": ("Burger", 6.50),
    "3": ("Salade César", 12.40),
    "4": ("Mangue", 3.20),
    "5": ("Steak", 14.95),
    "6": ("Tiramisu", 8.75)
}

# 0.1 + 0.2 - 0.3

budget = float(input("Quel est votre budget (€)? "))
commande = []
total = 0.0

while True:
    # Affichage du menu
    print("\n=== MENU ===")
    for menu_nb, (nom_produit, prix) in menu.items():
        print(f"{menu_nb}. {nom_produit} [Prix: €{prix:.2f}]")
    print(f"\nIl vous reste actuellement €{budget:.2f}")
    print(f"Total actuel de la commande: €{total:.2f}")

    # Récupération du choix utilisateur
    choix_utilisateur = input("Choisir un élément de la liste (0 pour arrêter): ")

    # Sortie de la boucle (l'utilisateur a fini de commandé)
    if choix_utilisateur == "0":
        break

    # L'utilisateur a choisi un article n'étant pas dans le menu
    if choix_utilisateur not in menu:
        print("Choix invalide")
        continue

    # L'utilisateur a choisi un article dans le menu
    nom_produit, prix_produit = menu[choix_utilisateur]

    if total + prix_produit > budget:
        print("Le budget est dépassé, choix impossible")
        continue

    commande.append(nom_produit)
    total += prix_produit
    print(f"Le produit '{nom_produit} a bien été ajouté à la commande'")

print("=== COMMANDE ===")
for produit in commande:
    print(f"- {produit}")
print(f"Total: €{total:.2f}")
print(f"Budget restant: €{budget - total:.2f}")