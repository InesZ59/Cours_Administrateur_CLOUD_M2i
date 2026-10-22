# Exercice Git #4 - Utilisation de Merge pour mettre à jour une branche 

## Objectif

Appréhender les branches ainsi que les merge dans un contexte de dépot local Git

## Sujet

Réaliser le scénario suivant via les commandes Git: 


* Créer un dépot local

```bash
mkdir exo-04

cd exo-04

git init
```

* Créer un fichier `README.md` et le commiter

```bash
touch README.md

git add README.md

git commit -m "Initial commit"
```

* Créer un dossier contenant un site web fictif avec un fichier de page d'accueil (`index.html`)

```bash
mkdir website

touch website/index.html
```

* Sauvegarder ces changements sur Git

```bash
git add website/index.html

git commit -m "Ajout de la page d'accueil
```

* Créer une branche `feat/about`

```bash
git branch feat/about
```

* Créer une branche `feat/api`

```bash
git branch feat/api

```

* Se placer sur `feat/about`

```bash
git switch feat/about
```

* Créer un fichier pour une page 'A propos'

```bash
git touch website/about.html
```

* Sauvegarder les changements sur Git

```bash
git add website/about.html

git commit -m website/about.html
```

* Se placer sur `feat/api`

```bash
git switch feat/api
```

* Créer une partie **backend** avec un potentiel fichier d'API

```bash
mkdir backend

touch backend/api.py
```

* Sauvegarder le changement sur Git

```bash
git add backend/api.py

git commit -m "Ajout du fichier de l'API"
```

* Dans la branche principale, ramener les changements des deux branches de feature

```bash
git switch master

git merge feat/about
git merge feat/api
```

* Vérifier l'historique des deux branches et observer leurs différences spécifiques

```bash
git log
```
