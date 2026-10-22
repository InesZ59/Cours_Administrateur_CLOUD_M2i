# Exercice Git #4 - Utilisation de Rebase pour mettre à jour une branche 

## Objectif

Appréhender les branches ainsi que les merge dans un contexte de dépot local Git

## Sujet

Réaliser le scénario suivant via les commandes Git: 


* Créer un dépot local

```bash
mkdir exo-05

cd exo-05

git init
```

* Créer un fichier `README.md` et le commiter

```bash
echo "# Exo 05" > README.md

git add README.md

git commit -m "Ajout du fichier README"
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

* Créer une branche `feat/contact`

```bash
git branch feat/contact
```

* Créer une branche `feat/api`

```bash
git branch feat/api

```

* Dans `feat/contact`, créer un fichier pour une page 'Contact'

```bash
git switch feat/contact

git touch website/contact.html

```

* Sauvegarder les changements sur Git

```bash
git add website/contact.html

git commit -m website/contact.html
```

* Dans `feat/api`, créer une partie **backend** avec un potentiel fichier d'API pour traiter la requête HTTP du formulaire de contact

```bash
git switch feat/api

mkdir backend

touch backend/api.py
```

* Sauvegarder le changement sur Git

```bash
git add backend/api.py

git commit -m "Ajout du fichier de l'API"
```

* Dans la branche principale, ramener les changements de la feature d'API via un merge

```bash
git switch master

git merge feat/api
```

* Dans la branche `feat/contact`, récupérer les changements liés à l'API

```bash
git switch feat/contact

git rebase master
```

* Vérifier l'historique des deux branches et observer leurs différences spécifiques (La branche de feature frontend doit avoir l'API mais pas l'inverse)

```bash
git log

git switch feat/api

git log
```
