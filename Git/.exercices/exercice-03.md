# Exercice Git #3 - Commit au mauvais endroit

## Objectif

Appréhender les commits et des branches ainsi que leur utilisation dans un contexte de dépot local Git

## Sujet

Réaliser le scénario suivant via les commandes Git: 


* Créer un dépot local

```bash
mkdir exo-03

cd exo-03

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

* Créer un fichier pour une page de contact ainsi qu'un fichier pour une page 'A propos'

```bash
touch website/contact.html

touch website/about.html
```

* Sauvegarder l'ensemble des changements sur Git

```bash
git add website/

git commit -m "Ajout des pages contact & à propos"
```

* Créer une partie fictive **backend** (un dossier) et y placer un potentiel fichier d'API

```bash
mkdir backend

touch backend/api.js
```

* Sauvegarder le changement sur Git

```bash
git add backend/api.js

git commit -m "Ajout de l'API"
```

* Oops! On vient de polluer la partie frontend avec du code provenant du backend. Corriger cela via les commandes Git

```bash
git reset --soft HEAD~1

git switch -c dev/backend

git commit -m "Ajout de l'API"
```

* Vérifier l'historique des deux branches et observer leurs différences spécifiques

```bash
git switch dev/backend

git log

git switch master

git log
```
