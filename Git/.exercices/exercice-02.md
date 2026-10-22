# Exercice Git #2 - Correction d'un commit de bogues

## Objectif

Appréhender les commits et leur utilisation dans un contexte de dépot local Git

## Sujet

Réaliser le scénario suivant via les commandes Git: 

* Créer un dépot local

```bash
mkdir exo-02

cd exo-02

git init
```

* Créer un dossier contenant un site web fictif avec un fichier de page d'accueil (`index.html`)

```bash
mkdir website

touch website/index.html
```

* Sauvegarder ces changements sur Git

```bash
git add website/index.html

git commit -m "Ajout de la page d'accueil"
```

* Créer un fichier induisant un bogue dans notre site web fictif

```bash
touch website/bogue.html
```

* Sauvegarder l'ensemble des changements sur Git

```bash
git add website/bogue.html

git commit -m "Ajout du bogue sur le dépot Git"
```

* Malheureusement, le bogue est désormais présent à la fois sur Git et sur notre machine. Faire en sorte de le retirer des deux emplacements en même temps via l'utilisation des commandes Git

```bash
git reset --hard HEAD~1
```

* Vérifier l'historique des commits Git et l'absence d'une sauvegarde du bogue dans notre branche principale

```bash
git log
```
