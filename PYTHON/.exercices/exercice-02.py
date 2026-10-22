print("=== MENU ===")
print("1. Coca Cola [Prix: €1.80]")
print("2. Burger [Prix: €6.50]")
print("3. Salade César [Prix: €12.40]")
print("4. Mangue [Prix: €3.20]")
print("5. Steak [Prix: €14.95]")
print("6. Tiramisu [Prix: €8.75]")

choix_utilisateur = input("Choisir un élément de la liste: ")

match choix_utilisateur:
    case "1":
        print("Vous allez devoir payer 1.80 euros !!!")
    case "2":
        print("Vous allez devoir payer 6.50 euros !!!")
    case "3":
        print("Vous allez devoir payer 12.40 euros !!!")
    case "4":
        print("Vous allez devoir payer 3.20 euros !!!")
    case "5":
        print("Vous allez devoir payer 14.95 euros !!!")
    case "6":
        print("Vous allez devoir payer 8.75 euros !!!")
    case _:
        print("Désolé, ce choix n'est pas disponible. Il faut choisir entre 1 et 6 compris...")