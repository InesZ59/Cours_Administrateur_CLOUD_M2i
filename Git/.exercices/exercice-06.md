# Exercice Git #6 - Utilisation de Merge pour mettre à jour une branche et résoudre les conflits

## Objectif

Appréhender les branches ainsi que les merge dans un contexte de dépot local Git

## Sujet

Réaliser le scénario suivant via les commandes Git: 


* Créer un dépot local

```bash
mkdir exo-06

cd exo-06

git init
```

* Créer un fichier `README.md` et le commiter

```bash
echo "# Exo 06" > README.md

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

* Créer un fichier pour une page 'A propos' (`about.html`) et y mettre un texte du style `Texte A`

```bash
echo "Texte A" > website/about.html
```

* Sauvegarder les changements sur Git

```bash
git add website/about.html

git commit -m "Ajout de la page d'à propos"
```

* Se placer sur `feat/api`

```bash
git switch feat/about

```

* Créer une partie **backend** avec un potentiel fichier d'API

```bash
mkdir backend

touch backend/api.py
```

* Créer le fichier de la page 'A propos' (`about.html`) et y mettre un texte du style `Texte B`

```bash
echo "Texte B" > website/about.html

```

* Sauvegarder le changement sur Git

```bash
git add website/about.html

git commit -m "Ajout de la page d'à propos"
```

* Dans la branche principale, ramener les changements des deux branches de feature

```bash
git switch master

git merge feat/api

git merge feat/about
```

* Résoudre les conflits via un commit de résolution de conflits

```bash
# Modifier le fichier website/about.html

git commit -am "Resolution du conflit"
```

* Vérifier l'historique des deux branches

```bash
git log 
```
