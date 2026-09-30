nombre_a = float(input("Veuillez donner le nombre A: "))
nombre_b = float(input("Veuillez donner le nombre B: "))

try:
    print(f"{nombre_a:.2f} / {nombre_b:.2f} = {nombre_a / nombre_b:.2f}")
except ZeroDivisionError:
    print("Attention, division par zéro. Pas content !")
except:
    print("Une erreur inconnue a eu lieu...")
finally:
    print("Je me produit en tout temps")