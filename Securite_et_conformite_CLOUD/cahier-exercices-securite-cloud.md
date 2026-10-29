# Sécurité cloud — cahier d'exercices

> Module CL-SECU en 2 jours · AWS CloudShell, région Paris (Azure Cloud Shell pour les bonus facultatifs)

Copiez les commandes avec le bouton **Copier** de la version HTML de ce cahier, jamais depuis le PDF.

## Sommaire

- Exercice 0 — Mise en route : AWS CloudShell
- Exercice 1 — Le moindre privilège, prouvé avant d'être appliqué
- Exercice 2 — Le port SSH ouvert au monde : créer, détecter, corriger
- Exercice 3 — Des données qui ne fuient pas, un secret bien rangé
- Exercice 4 — Qui a fait quoi ? Enquêter dans les journaux
- Exercice 5 — Réponse à incident : une clé a fuité
- Nettoyage de fin de module — ne rien laisser derrière soi
- Annexe — Démo — Surveiller : l'audit express du compte et ce que voit GuardDuty

<div style="page-break-before: always"></div>

# Exercice 0 — Mise en route : AWS CloudShell

> Module : 15 — CL-SECU (version 2 jours) · Jour 1
> Durée estimée : 15 min
> Difficulté : 1 / 5
> Type : Prise en main

## Objectifs pédagogiques

À la fin de cette mise en route, vous saurez :

- ouvrir **AWS CloudShell**, un terminal déjà connecté à votre compte, directement dans le navigateur ;
- vérifier que vos accès fonctionnent avant de commencer les exercices.

## Les règles de tous les exercices du module

1. **Rien à installer** : toutes les commandes se tapent dans **AWS CloudShell**, un terminal déjà connecté à votre compte, directement dans le navigateur.
2. Chaque bloc de commandes commence par une ligne qui dit **où** le coller :
   - `# [AWS CloudShell]` : dans AWS CloudShell, région **Paris (eu-west-3)** ;
   - `# [Azure Cloud Shell]` : dans Azure Cloud Shell, en mode **Bash**. Ces blocs n'apparaissent que dans les sections **« Bonus Azure (facultatif) »**, pour ceux qui ont terminé en avance.
3. Chaque bloc **recalcule lui-même** vos variables (votre nom d'utilisateur, votre numéro de compte…) à partir du compte connecté : vous n'avez **rien à remplacer**.
4. Copiez-collez chaque bloc **en entier**. Les vérifications affichent `OK` ou `ERREUR`.
5. Chaque ressource que vous créez porte votre nom (`secu-user7-…`). **Ne modifiez jamais une ressource qui ne porte pas votre nom** : vous partagez le compte AWS avec toute la promotion.
6. En fin de jour 2, le nettoyage supprime tout ce que vous avez créé.

## Partie 1 — AWS CloudShell

1. Connectez-vous à la console AWS : **https://639962416620.signin.aws.amazon.com/console**, type « Utilisateur IAM », avec votre identifiant `userN` et votre mot de passe.
2. En haut à droite, choisissez la région **Europe (Paris) eu-west-3**.
3. Cliquez sur l'icône **CloudShell** (le symbole `>_` en haut de la console). Attendez l'invite `[cloudshell-user@ip-… ~]$`.

Collez ce bloc :

```bash
# [AWS CloudShell]
export AWS_REGION=eu-west-3
P=$(aws sts get-caller-identity --query Arn --output text | awk -F/ '{print $NF}')
COMPTE=$(aws sts get-caller-identity --query Account --output text)
echo "Utilisateur : $P | Compte : $COMPTE | Région : $AWS_REGION"
if aws iam get-user --user-name "$P" > /dev/null 2>&1; then echo "OK : identité AWS reconnue ($P)"; else echo "ERREUR : identité AWS non reconnue (appelez le formateur)"; fi
```

```text
Utilisateur : user7 | Compte : 639962416620 | Région : eu-west-3
OK : identité AWS reconnue (user7)
```

## Bonus Azure (facultatif) — Azure Cloud Shell

1. Connectez-vous au portail **https://portal.azure.com** avec votre compte `stagiaireNN@utopios.onmicrosoft.com`.
2. Cliquez sur l'icône **Cloud Shell** (`>_` en haut du portail), choisissez **Bash**.
3. À la première ouverture, choisissez **« Aucun compte de stockage requis »**, puis l'abonnement **formation**.

> Azure Cloud Shell est déjà authentifié avec la MFA du portail : c'est pour cela qu'on l'utilise ici plutôt que la CLI de votre WSL, où les créations de ressources sont refusées sans MFA.

Collez ce bloc :

```bash
# [Azure Cloud Shell]
U=$(az account show --query user.name -o tsv); N=${U%%@*}; RG=rg-${N//./-}
echo "Utilisateur : $U | Groupe de ressources : $RG"
if az group show -n "$RG" > /dev/null 2>&1; then echo "OK : groupe de ressources $RG accessible"; else echo "ERREUR : groupe de ressources $RG introuvable (appelez le formateur)"; fi
```

```text
Utilisateur : stagiaire07@utopios.onmicrosoft.com | Groupe de ressources : rg-stagiaire07
OK : groupe de ressources rg-stagiaire07 accessible
```

## Dépannage

| Symptôme | Solution |
|---|---|
| CloudShell indique une autre région | Choisissez « Europe (Paris) » en haut à droite **avant** d'ouvrir CloudShell, ou gardez la ligne `export AWS_REGION=eu-west-3` de chaque bloc |
| Azure : `ERREUR : groupe de ressources … introuvable` | Votre groupe a peut-être été supprimé : demandez au formateur de le recréer |
| Azure Cloud Shell demande de créer un stockage | Choisissez « Aucun compte de stockage requis » (session éphémère) |
| Une session CloudShell expire (inactivité) | Rouvrez-la : chaque bloc recalcule ses variables, rien n'est perdu |

<div style="page-break-before: always"></div>

# Exercice 1 — Le moindre privilège, prouvé avant d'être appliqué

> Module : 15 — CL-SECU (version 2 jours) · Jour 1
> Durée estimée : 35 min
> Difficulté : 2 / 5
> Type : Exercice d'application

## Objectifs pédagogiques

- Repérer une politique trop large grâce à un **outil**, pas à l'intuition.
- Écrire une politique IAM limitée à **une** ressource et **deux** actions.
- **Prouver** ce qu'une politique autorise ou refuse, **sans** l'attacher à personne.

## Contexte

Un développeur demande « les droits S3 » pour qu'un script lise des rapports dans **un** bucket. La tentation : `s3:*` sur `*`. Votre mission : lui donner exactement ce dont il a besoin, et le **prouver**. Rien n'est créé dans le compte pendant cet exercice : tout se passe dans des fichiers et des simulations.

## Partie 1 — Faire juger une politique trop large (AWS)

**IAM Access Analyzer** sait relire une politique et signaler les erreurs et les risques. On lui soumet la politique « confortable » qu'on voit trop souvent.

```bash
# [AWS CloudShell]
export AWS_REGION=eu-west-3
cat > politique-trop-large.json <<'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:*", "iam:PassRole"],
      "Resource": "*"
    }
  ]
}
EOF
aws accessanalyzer validate-policy --policy-type IDENTITY_POLICY --policy-document file://politique-trop-large.json --query "findings[].[findingType,issueCode]" --output table
```

Résultat attendu :

```text
---------------------------------------------------------
|                    ValidatePolicy                     |
+-------------------+-----------------------------------+
|  SECURITY_WARNING |  PASS_ROLE_WITH_STAR_IN_RESOURCE  |
+-------------------+-----------------------------------+
```

Un constat `SECURITY_WARNING` de type `PASS_ROLE_WITH_STAR_IN_RESOURCE`. Avec `iam:PassRole` sur `*`, le script pourrait confier **n'importe quel rôle du compte** à un service, y compris un rôle administrateur.

Deuxième essai : une faute de frappe dans un nom d'action.

```bash
# [AWS CloudShell]
export AWS_REGION=eu-west-3
cat > politique-faute.json <<'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    { "Effect": "Allow", "Action": "s3:GetObjet", "Resource": "*" }
  ]
}
EOF
aws accessanalyzer validate-policy --policy-type IDENTITY_POLICY --policy-document file://politique-faute.json --query "findings[].[findingType,issueCode]" --output table
```

Résultat attendu :

```text
-----------------------------
|      ValidatePolicy       |
+--------+------------------+
|  ERROR |  INVALID_ACTION  |
+--------+------------------+
```

L'action inconnue `s3:GetObjet` est signalée comme une **erreur**. IAM, lui, aurait accepté cette politique sans broncher : elle n'aurait simplement **rien** autorisé.

## Partie 2 — Écrire la politique au moindre privilège (AWS)

Le bucket du script s'appelle `secu-<votre-utilisateur>-<numéro-de-compte>` (vous le créerez vous-même à l'exercice 3). Le script doit **lister** ce bucket et **lire** ses objets, rien d'autre.

> Remarquez le `<<EOF` **sans** apostrophes : le shell remplace `$BUCKET` par sa valeur dans le fichier.

```bash
# [AWS CloudShell]
export AWS_REGION=eu-west-3
P=$(aws sts get-caller-identity --query Arn --output text | awk -F/ '{print $NF}')
COMPTE=$(aws sts get-caller-identity --query Account --output text)
BUCKET="secu-$P-$COMPTE"
cat > politique-lecture-bucket.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ListerLeBucket",
      "Effect": "Allow",
      "Action": "s3:ListBucket",
      "Resource": "arn:aws:s3:::$BUCKET"
    },
    {
      "Sid": "LireLesObjets",
      "Effect": "Allow",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::$BUCKET/*"
    }
  ]
}
EOF
cat politique-lecture-bucket.json
NB=$(aws accessanalyzer validate-policy --policy-type IDENTITY_POLICY --policy-document file://politique-lecture-bucket.json --query "length(findings)" --output text)
if [ "$NB" = "0" ]; then echo "OK : Access Analyzer ne relève aucun problème"; else echo "ERREUR : $NB constat(s), relisez la politique"; fi
```

Résultat attendu : la politique affichée avec **votre** nom de bucket, puis `OK : Access Analyzer ne relève aucun problème`.

## Partie 3 — Prouver ce que la politique autorise (AWS)

Le **simulateur de politiques** répond à la question « cette politique autorise-t-elle telle action sur telle ressource ? » **sans** rien attacher et **sans** rien exécuter.

> Le simulateur attend une **liste** de politiques, chacune sous forme de **texte**. `jq -c "[tojson]"` transforme votre fichier en une telle liste (`["{…la politique…}"]`).

```bash
# [AWS CloudShell]
export AWS_REGION=eu-west-3
P=$(aws sts get-caller-identity --query Arn --output text | awk -F/ '{print $NF}')
COMPTE=$(aws sts get-caller-identity --query Account --output text)
BUCKET="secu-$P-$COMPTE"
echo "--- Sur VOTRE bucket ---"
aws iam simulate-custom-policy --policy-input-list "$(jq -c "[tojson]" politique-lecture-bucket.json)" --action-names s3:GetObject s3:PutObject s3:DeleteObject --resource-arns "arn:aws:s3:::$BUCKET/rapport.csv" --query "EvaluationResults[].[EvalActionName,EvalDecision]" --output table
echo "--- Sur un AUTRE bucket ---"
aws iam simulate-custom-policy --policy-input-list "$(jq -c "[tojson]" politique-lecture-bucket.json)" --action-names s3:GetObject --resource-arns "arn:aws:s3:::un-autre-bucket/rapport.csv" --query "EvaluationResults[].[EvalActionName,EvalDecision]" --output table
```

Résultat attendu :

```text
--- Sur VOTRE bucket ---
-----------------------------------
|      SimulateCustomPolicy       |
+-----------------+---------------+
|  s3:GetObject   |  allowed      |
|  s3:PutObject   |  implicitDeny |
|  s3:DeleteObject|  implicitDeny |
+-----------------+---------------+
--- Sur un AUTRE bucket ---
...
|  s3:GetObject   |  implicitDeny |
```

`implicitDeny` = refusé **par défaut**, parce que rien ne l'autorise. C'est le principe d'IAM : tout ce qui n'est pas explicitement permis est interdit.

## Questions

1. Pourquoi Access Analyzer signale-t-il `iam:PassRole` sur `*`, alors qu'il ne dit rien de `s3:*` sur `*` ?
2. Dans la partie 3, quelle est la différence entre `implicitDeny` et `explicitDeny` ? Comment obtiendriez-vous un `explicitDeny` ?

## Indice

<details>
<summary>Indice question 1</summary>

Access Analyzer ne juge pas l'**ampleur** des droits (c'est votre travail de concepteur), il signale des **schémas reconnus comme dangereux** : `iam:PassRole` sur `*` permet une élévation de privilèges.

</details>

## Pour aller plus loin (bonus)

Ajoutez à la politique de la partie 2 une **condition** qui n'autorise la lecture que si la requête arrive en HTTPS (`"Condition": {"Bool": {"aws:SecureTransport": "true"}}`), puis relancez la simulation avec `--context-entries "ContextKeyName=aws:SecureTransport,ContextKeyValues=false,ContextKeyType=boolean"`.

## Bonus Azure (facultatif) — lire ce que permet un rôle

Sur Azure, on n'écrit généralement pas de politique : on **choisit un rôle** (intégré ou personnalisé) et une **portée**. Regardez d'abord vos propres rôles :

```bash
# [Azure Cloud Shell]
U=$(az account show --query user.name -o tsv); N=${U%%@*}; RG=rg-${N//./-}
az role assignment list -g "$RG" --assignee "$U" --include-inherited --query "[].{role:roleDefinitionName, portee:scope}" -o table
```

Puis comparez ce que permettent trois rôles intégrés. Un rôle a des **actions** (le plan de contrôle : créer, configurer, supprimer des ressources) et des **dataActions** (le plan de données : lire ou écrire le **contenu**, comme les fichiers d'un stockage ou les secrets d'un coffre).

```bash
# [Azure Cloud Shell]
U=$(az account show --query user.name -o tsv); N=${U%%@*}; RG=rg-${N//./-}
PORTEE=$(az group show -n "$RG" --query id -o tsv)
for role in "Reader" "Contributor" "Storage Blob Data Reader"; do
  echo "=== $role"
  az role definition list --name "$role" --scope "$PORTEE" --query "[0].permissions[0].{actions:actions, notActions:notActions, dataActions:dataActions}" -o json
done
```

Questions du bonus :

1. Le rôle `Contributor` a l'action `*`. Pourquoi ne permet-il pas, à lui seul, de lire le contenu d'un blob (`dataActions` vide) ? Et pourtant, un `Contributor` peut lire les blobs d'un compte de stockage : par quel détour ? (Indice : `Microsoft.Storage/storageAccounts/listKeys/action`.)
2. Quel est votre rôle sur votre groupe de ressources ? Pourquoi ne pouvez-vous pas vous attribuer le rôle `Owner` ?

<div style="page-break-before: always"></div>

# Exercice 2 — Le port SSH ouvert au monde : créer, détecter, corriger

> Module : 15 — CL-SECU (version 2 jours) · Jour 1
> Durée estimée : 30 min
> Difficulté : 2 / 5
> Type : Exercice d'application

## Objectifs pédagogiques

- Reconnaître la mauvaise configuration réseau la plus répandue du cloud : SSH (port 22) ouvert à `0.0.0.0/0`.
- La **détecter par une requête**, sur tout un compte ou un abonnement, et pas en cliquant groupe par groupe.
- La **corriger** en restreignant la source à une adresse d'administration.

## Contexte

« Je n'arrivais pas à me connecter, j'ai ouvert le 22 à tout le monde, c'était plus simple. » Cette phrase est à l'origine d'une grande partie des machines compromises par des robots qui balaient Internet en permanence. Vous allez reproduire l'erreur **sur un groupe vide qui vous appartient**, apprendre à la retrouver partout, puis la corriger.

> ⚠️ Vous ne modifiez **que** le groupe qui porte votre nom. Les autres groupes du compte appartiennent à d'autres personnes : on les **observe**, on ne les touche pas.

## Partie 1 — Reproduire l'erreur (AWS)

On crée un **security group** vide, dans le VPC par défaut de la région de Paris, puis on y ouvre le port 22 à tout Internet. Aucune machine n'y est rattachée : c'est sans risque.

```bash
# [AWS CloudShell]
export AWS_REGION=eu-west-3

P=$(aws sts get-caller-identity --query Arn --output text | awk -F/ '{print $NF}')

VPC=$(aws ec2 describe-vpcs --filters Name=isDefault,Values=true --query "Vpcs[0].VpcId" --output text)

SG=$(aws ec2 describe-security-groups --filters Name=group-name,Values="secu-$P-sg" --query "SecurityGroups[0].GroupId" --output text)

if [ "$SG" = "None" ]; then
  SG=$(aws ec2 create-security-group --group-name "secu-$P-sg" --description "Exercice CL-SECU de $P" --vpc-id "$VPC" --query GroupId --output text)
fi

if aws ec2 authorize-security-group-ingress --group-id "$SG" --protocol tcp --port 22 --cidr 0.0.0.0/0 > /dev/null 2>&1; then echo "Règle ajoutée : port 22 ouvert à 0.0.0.0/0"; else echo "Règle déjà présente"; fi

aws ec2 describe-security-groups --group-ids "$SG" --query "SecurityGroups[0].IpPermissions[].{port:FromPort, sources:IpRanges[].CidrIp}" --output json
```

Résultat attendu : `Règle ajoutée…`, puis la règle `port 22` avec la source `0.0.0.0/0`.

## Partie 2 — Détecter, à l'échelle du compte (AWS)

Un auditeur ne regarde pas les groupes un par un : il **interroge** l'API avec des filtres.

```bash
# [AWS CloudShell]
export AWS_REGION=eu-west-3
P=$(aws sts get-caller-identity --query Arn --output text | awk -F/ '{print $NF}')
echo "--- Groupes du compte avec le port 22 ouvert à tout Internet (20 premiers) ---"
aws ec2 describe-security-groups --filters Name=ip-permission.from-port,Values=22 Name=ip-permission.cidr,Values=0.0.0.0/0 --query "SecurityGroups[].[GroupId,GroupName]" --output text | head -n 20
NB=$(aws ec2 describe-security-groups --filters Name=ip-permission.from-port,Values=22 Name=ip-permission.cidr,Values=0.0.0.0/0 --query "length(SecurityGroups)" --output text)
TOTAL=$(aws ec2 describe-security-groups --query "length(SecurityGroups)" --output text)
echo "Bilan : $NB groupes sur $TOTAL exposent SSH à Internet dans la région"
if aws ec2 describe-security-groups --filters Name=ip-permission.from-port,Values=22 Name=ip-permission.cidr,Values=0.0.0.0/0 --query "SecurityGroups[].GroupName" --output text | grep -qw "secu-$P-sg"; then echo "OK : votre groupe secu-$P-sg est bien détecté"; else echo "ERREUR : votre groupe n'est pas détecté (refaites la partie 1)"; fi
```

Résultat attendu : une liste de groupes (des dizaines !), le bilan, et `OK : votre groupe … est bien détecté`.

## Partie 3 — Corriger (AWS)

La correction : retirer la règle ouverte à tous et n'autoriser **que** l'adresse d'administration. Ici, on prend l'adresse IP publique de votre CloudShell, que donne le service `checkip.amazonaws.com`.

```bash
# [AWS CloudShell]
export AWS_REGION=eu-west-3
P=$(aws sts get-caller-identity --query Arn --output text | awk -F/ '{print $NF}')
SG=$(aws ec2 describe-security-groups --filters Name=group-name,Values="secu-$P-sg" --query "SecurityGroups[0].GroupId" --output text)
MON_IP=$(curl -s https://checkip.amazonaws.com)
echo "Adresse d'administration : $MON_IP"
aws ec2 revoke-security-group-ingress --group-id "$SG" --protocol tcp --port 22 --cidr 0.0.0.0/0 > /dev/null 2>&1 || true
aws ec2 authorize-security-group-ingress --group-id "$SG" --protocol tcp --port 22 --cidr "$MON_IP/32" > /dev/null 2>&1 || true
aws ec2 describe-security-groups --group-ids "$SG" --query "SecurityGroups[0].IpPermissions[].{port:FromPort, sources:IpRanges[].CidrIp}" --output json
if aws ec2 describe-security-groups --group-ids "$SG" --query "SecurityGroups[0].IpPermissions[].IpRanges[].CidrIp" --output text | grep -q "0.0.0.0/0"; then echo "ERREUR : le port 22 est encore ouvert à tout Internet"; else echo "OK : le port 22 n'est plus ouvert qu'à $MON_IP/32"; fi
```

## Questions

1. Combien de groupes du compte AWS exposent SSH à tout Internet ? Pourquoi un auditeur doit-il quand même vérifier chaque cas avant de crier au scandale ?
2. Restreindre la source à une adresse IP, est-ce suffisant ? Citez une alternative qui évite d'ouvrir le port 22 du tout.

<details>
<summary>Indice question 2</summary>

AWS : Session Manager (Systems Manager) ou EC2 Instance Connect Endpoint. Azure : Azure Bastion.

</details>

## Bonus Azure (facultatif) — le NSG ouvert

Sur Azure, l'équivalent du security group est le **NSG** (Network Security Group). Même scénario, dans **votre** groupe de ressources.

```bash
# [Azure Cloud Shell]
U=$(az account show --query user.name -o tsv); N=${U%%@*}; RG=rg-${N//./-}
az network nsg create -g "$RG" -n nsg-secu-audit -o none
az network nsg rule create -g "$RG" --nsg-name nsg-secu-audit -n ssh-ouvert --priority 100 --direction Inbound --access Allow --protocol Tcp --source-address-prefixes '*' --destination-port-ranges 22 -o none
echo "--- Règles entrantes ouvertes à tout Internet dans $RG ---"
az network nsg list -g "$RG" --query "[].securityRules[?direction=='Inbound' && access=='Allow' && (sourceAddressPrefix=='*' || sourceAddressPrefix=='Internet' || sourceAddressPrefix=='0.0.0.0/0')][].{regle:name, port:destinationPortRange, source:sourceAddressPrefix}" -o table
```

Résultat attendu : la règle `ssh-ouvert` avec la source `*`, et peut-être d'autres règles de vos NSG précédents (les VM créées dans le portail ouvrent souvent SSH à tous par défaut).

La correction :

```bash
# [Azure Cloud Shell]
U=$(az account show --query user.name -o tsv); N=${U%%@*}; RG=rg-${N//./-}
MON_IP=$(curl -s https://api.ipify.org)
echo "Adresse d'administration : $MON_IP"
az network nsg rule update -g "$RG" --nsg-name nsg-secu-audit -n ssh-ouvert --source-address-prefixes "$MON_IP/32" -o none
SOURCE=$(az network nsg rule show -g "$RG" --nsg-name nsg-secu-audit -n ssh-ouvert --query sourceAddressPrefix -o tsv)
if [ "$SOURCE" = "$MON_IP/32" ]; then echo "OK : la règle ssh-ouvert n'accepte plus que $SOURCE"; else echo "ERREUR : source actuelle = $SOURCE"; fi
```

<div style="page-break-before: always"></div>

# Exercice 3 — Des données qui ne fuient pas, un secret bien rangé

> Module : 15 — CL-SECU (version 2 jours) · Jour 1
> Durée estimée : 50 min
> Difficulté : 2 / 5
> Type : Exercice d'application

## Objectifs pédagogiques

- Vérifier les protections d'un bucket S3 : **blocage de l'accès public**, **chiffrement**, **HTTPS obligatoire**.
- **Prouver** par un test qu'un fichier n'est pas lisible anonymement, et le partager **temporairement** avec une URL présignée.
- Constater que le garde-fou refuse de rendre le bucket public.
- Ranger un mot de passe **chiffré** dans un coffre, au lieu de l'écrire dans un fichier.

## Contexte

Les buckets S3 ouverts au public sont la première source de fuites de données dans le cloud, et les mots de passe écrits en clair dans des fichiers ou des dépôts Git la deuxième. Les fournisseurs ont fini par **bloquer l'accès public par défaut** : encore faut-il savoir le vérifier, savoir partager un fichier proprement, et ranger ses secrets dans un coffre.

## Partie 1 — Créer et inspecter un bucket (AWS)

Le nom d'un bucket est **unique au monde** : on y met votre nom d'utilisateur et le numéro du compte.

```bash
# [AWS CloudShell]
export AWS_REGION=eu-west-3
P=$(aws sts get-caller-identity --query Arn --output text | awk -F/ '{print $NF}')
COMPTE=$(aws sts get-caller-identity --query Account --output text)
BUCKET="secu-$P-$COMPTE"
if ! aws s3api head-bucket --bucket "$BUCKET" 2> /dev/null; then
  aws s3api create-bucket --bucket "$BUCKET" --create-bucket-configuration LocationConstraint=eu-west-3 > /dev/null
fi
echo "--- Blocage de l'accès public ---"
aws s3api get-public-access-block --bucket "$BUCKET" --query PublicAccessBlockConfiguration --output table
echo "--- Chiffrement par défaut ---"
aws s3api get-bucket-encryption --bucket "$BUCKET" --query "ServerSideEncryptionConfiguration.Rules[0].ApplyServerSideEncryptionByDefault" --output table
```

Résultat attendu : les 4 réglages du blocage d'accès public à `True`, et un chiffrement `AES256` (SSE-S3). Depuis 2023, AWS les active **par défaut** sur tout nouveau bucket.

## Partie 2 — Imposer HTTPS et déposer un fichier (AWS)

Une **politique de bucket** (attachée au bucket, et non à un utilisateur) **refuse** toute requête qui n'arrive pas en HTTPS. Un `Deny` explicite l'emporte toujours sur un `Allow`.

```bash
# [AWS CloudShell]
export AWS_REGION=eu-west-3
P=$(aws sts get-caller-identity --query Arn --output text | awk -F/ '{print $NF}')
COMPTE=$(aws sts get-caller-identity --query Account --output text)
BUCKET="secu-$P-$COMPTE"
cat > politique-bucket.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "RefuserSansHTTPS",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": ["arn:aws:s3:::$BUCKET", "arn:aws:s3:::$BUCKET/*"],
      "Condition": { "Bool": { "aws:SecureTransport": "false" } }
    }
  ]
}
EOF
aws s3api put-bucket-policy --bucket "$BUCKET" --policy file://politique-bucket.json
echo "Rapport confidentiel de test - $(date)" > rapport.csv
aws s3 cp rapport.csv "s3://$BUCKET/rapport.csv" --only-show-errors
echo "Politique HTTPS appliquée, fichier rapport.csv déposé dans $BUCKET"
```

## Partie 3 — Prouver que le fichier n'est pas public (AWS)

```bash
# [AWS CloudShell]
export AWS_REGION=eu-west-3
P=$(aws sts get-caller-identity --query Arn --output text | awk -F/ '{print $NF}')
COMPTE=$(aws sts get-caller-identity --query Account --output text)
BUCKET="secu-$P-$COMPTE"
CODE=$(curl -s -o /dev/null -w "%{http_code}" "https://$BUCKET.s3.eu-west-3.amazonaws.com/rapport.csv")
if [ "$CODE" = "403" ]; then echo "OK : accès anonyme refusé (HTTP $CODE)"; else echo "ERREUR : accès anonyme a répondu HTTP $CODE"; fi
URL=$(aws s3 presign "s3://$BUCKET/rapport.csv" --expires-in 300)
echo "URL présignée (valable 5 minutes) : ${URL:0:80}..."
CODE=$(curl -s -o /dev/null -w "%{http_code}" "$URL")
if [ "$CODE" = "200" ]; then echo "OK : l'URL présignée donne accès au fichier (HTTP $CODE)"; else echo "ERREUR : l'URL présignée a répondu HTTP $CODE"; fi
CODE=$(curl -s -o /dev/null -w "%{http_code}" "${URL/https:/http:}")
if [ "$CODE" = "403" ]; then echo "OK : la même URL en HTTP (sans chiffrement) est refusée (HTTP $CODE)"; else echo "ERREUR : la même URL en HTTP a répondu HTTP $CODE"; fi
```

Résultat attendu :

```text
OK : accès anonyme refusé (HTTP 403)
URL présignée (valable 5 minutes) : https://secu-user7-639962416620.s3.eu-west-3.amazonaws.com/rapport.csv?...
OK : l'URL présignée donne accès au fichier (HTTP 200)
OK : la même URL en HTTP (sans chiffrement) est refusée (HTTP 403)
```

## Partie 4 — Le garde-fou en action (AWS)

Essayons maintenant de faire **l'erreur** : rendre le bucket lisible par tout le monde avec une politique publique.

```bash
# [AWS CloudShell]
export AWS_REGION=eu-west-3
P=$(aws sts get-caller-identity --query Arn --output text | awk -F/ '{print $NF}')
COMPTE=$(aws sts get-caller-identity --query Account --output text)
BUCKET="secu-$P-$COMPTE"
cat > politique-publique.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    { "Sid": "LectureParTous", "Effect": "Allow", "Principal": "*", "Action": "s3:GetObject", "Resource": "arn:aws:s3:::$BUCKET/*" }
  ]
}
EOF
if aws s3api put-bucket-policy --bucket "$BUCKET" --policy file://politique-publique.json 2> erreur.txt; then
  echo "ERREUR : la politique publique a été acceptée !"
else
  echo "OK : le blocage de l'accès public a refusé la politique publique :"
  cat erreur.txt
fi
```

Résultat attendu : `OK : le blocage de l'accès public a refusé…`, suivi d'un message `AccessDenied` qui cite `BlockPublicPolicy`.

## Partie 5 — Ranger un secret : Parameter Store

**Parameter Store** (service Systems Manager) stocke des paramètres de configuration. Le type **`SecureString`** les chiffre avec une clé **KMS** (Key Management Service). On génère un mot de passe aléatoire, sans jamais le taper ni l'afficher.

```bash
# [AWS CloudShell]
export AWS_REGION=eu-west-3
P=$(aws sts get-caller-identity --query Arn --output text | awk -F/ '{print $NF}')
aws ssm put-parameter --name "/secu/$P/db-mot-de-passe" --type SecureString --value "$(openssl rand -hex 16)" --overwrite --query Version --output text
echo "--- Lecture SANS déchiffrement ---"
aws ssm get-parameter --name "/secu/$P/db-mot-de-passe" --query "Parameter.Type" --output text
aws ssm get-parameter --name "/secu/$P/db-mot-de-passe" --query "Parameter.Value" --output text | cut -c1-70
```

Résultat attendu : un numéro de version, le type `SecureString`, puis le début d'une valeur **illisible** (une longue chaîne qui commence par `AQICA…`) : c'est le texte chiffré.

```bash
# [AWS CloudShell]
export AWS_REGION=eu-west-3
P=$(aws sts get-caller-identity --query Arn --output text | awk -F/ '{print $NF}')
echo "--- Lecture AVEC déchiffrement (il faut le droit kms:Decrypt) ---"
aws ssm get-parameter --name "/secu/$P/db-mot-de-passe" --with-decryption --query Parameter.Value --output text
echo "--- Rotation : nouvelle valeur, nouvelle version ---"
aws ssm put-parameter --name "/secu/$P/db-mot-de-passe" --type SecureString --value "$(openssl rand -hex 16)" --overwrite --query Version --output text
aws ssm get-parameter-history --name "/secu/$P/db-mot-de-passe" --query "Parameters[].{version:Version, modifie_le:LastModifiedDate, par:LastModifiedUser}" --output table
```

Résultat attendu : le mot de passe en clair (32 caractères hexadécimaux), puis un historique de **deux** versions, avec la date et **l'identité** de l'auteur de chaque version.

## Questions

1. Le fichier est chiffré au repos (AES256). Pourquoi cela ne protège-t-il **pas** contre une fuite par un bucket public ?
2. Quelle différence entre une URL présignée et un bucket public ? Qui peut utiliser l'URL, et pendant combien de temps ?
3. Qui peut lire la valeur **chiffrée** d'un `SecureString` ? Qui peut lire la valeur **déchiffrée** ? Quelle permission fait la différence ?
4. Votre application doit lire ce secret. Pourquoi ne faut-il **pas** lui donner une clé d'accès pour le faire ? Quel mécanisme utiliser à la place ?

## Bonus Azure (facultatif) — compte de stockage durci

Sur Azure, le stockage objet s'appelle **Blob Storage**, dans un **compte de stockage** (nom unique au monde, 24 caractères maximum, minuscules et chiffres). On le crée **directement** durci : HTTPS seulement, TLS 1.2 minimum, accès public aux blobs **interdit**.

```bash
# [Azure Cloud Shell]
U=$(az account show --query user.name -o tsv); N=${U%%@*}; RG=rg-${N//./-}
LOC=$(az group show -n "$RG" --query location -o tsv)
ST=stsecu$(echo -n "$U" | md5sum | cut -c1-12)
echo "Compte de stockage : $ST (région $LOC)"
az storage account create -n "$ST" -g "$RG" -l "$LOC" --sku Standard_LRS --kind StorageV2 --https-only true --min-tls-version TLS1_2 --allow-blob-public-access false -o none
az storage account show -n "$ST" -g "$RG" --query "{httpsSeulement:enableHttpsTrafficOnly, tlsMin:minimumTlsVersion, accesPublicBlobs:allowBlobPublicAccess, chiffrement:encryption.services.blob.enabled}" -o table
CLE=$(az storage account keys list -n "$ST" -g "$RG" --query "[0].value" -o tsv)
az storage container create -n donnees --account-name "$ST" --account-key "$CLE" -o none
echo "Rapport confidentiel de test - $(date)" > rapport.csv
az storage blob upload --account-name "$ST" --account-key "$CLE" -c donnees -n rapport.csv -f rapport.csv --overwrite --no-progress -o none
echo "Fichier déposé"
```

Prouver que le fichier n'est pas public, le partager avec un **jeton SAS** (Shared Access Signature, l'équivalent de l'URL présignée), puis tenter de rendre le conteneur public :

```bash
# [Azure Cloud Shell]
U=$(az account show --query user.name -o tsv); N=${U%%@*}; RG=rg-${N//./-}
ST=stsecu$(echo -n "$U" | md5sum | cut -c1-12)
CLE=$(az storage account keys list -n "$ST" -g "$RG" --query "[0].value" -o tsv)
CODE=$(curl -s -o /dev/null -w "%{http_code}" "https://$ST.blob.core.windows.net/donnees/rapport.csv")
if [ "$CODE" = "409" ] || [ "$CODE" = "404" ]; then echo "OK : accès anonyme refusé (HTTP $CODE)"; else echo "ERREUR : accès anonyme a répondu HTTP $CODE"; fi
FIN=$(date -u -d "+10 minutes" +%Y-%m-%dT%H:%MZ)
URL=$(az storage blob generate-sas --account-name "$ST" --account-key "$CLE" -c donnees -n rapport.csv --permissions r --expiry "$FIN" --https-only --full-uri -o tsv)
CODE=$(curl -s -o /dev/null -w "%{http_code}" "$URL")
if [ "$CODE" = "200" ]; then echo "OK : le jeton SAS (lecture seule, 10 min) donne accès au fichier (HTTP $CODE)"; else echo "ERREUR : le jeton SAS a répondu HTTP $CODE"; fi
if az storage container set-permission -n donnees --public-access blob --account-name "$ST" --account-key "$CLE" -o none 2> erreur.txt; then
  echo "ERREUR : le conteneur a pu être rendu public !"
else
  echo "OK : le compte refuse de rendre le conteneur public :"
  head -n 3 erreur.txt
fi
```

<div style="page-break-before: always"></div>

# Exercice 4 — Qui a fait quoi ? Enquêter dans les journaux

> Module : 15 — CL-SECU (version 2 jours) · Jour 2
> Durée estimée : 35 min
> Difficulté : 2 / 5
> Type : Exercice d'application

## Objectifs pédagogiques

- Interroger le journal des appels d'API d'AWS : **CloudTrail**.
- Retrouver ses **propres** actions de la veille : qui, quoi, quand, depuis où.
- Lire un événement complet et en extraire les informations utiles à une enquête.

## Contexte

Hier, vous avez ouvert un port SSH au monde, créé un bucket, rangé un secret. Tout cela a laissé des traces. Aujourd'hui, vous êtes l'enquêteur : sans rien savoir d'autre que votre nom d'utilisateur, retrouvez **toutes** vos actions.

> Les événements apparaissent dans CloudTrail avec **5 à 15 minutes** de délai. Les actions d'hier sont toutes disponibles.

## Partie 1 — AWS : vos actions qui ont modifié quelque chose

**CloudTrail** enregistre chaque appel d'API du compte (console, CLI, scripts) et garde **90 jours** d'historique, sans aucun réglage (*Event history*). Les lectures (`Describe…`, `Get…`, `List…`) sont très nombreuses : on ne garde que les événements marqués `"readOnly":false`, ceux qui **modifient** quelque chose.

```bash
# [AWS CloudShell]
export AWS_REGION=eu-west-3
P=$(aws sts get-caller-identity --query Arn --output text | awk -F/ '{print $NF}')
DEBUT=$(date -u -d "-2 days" +%Y-%m-%dT%H:%M:%SZ)
aws cloudtrail lookup-events --lookup-attributes AttributeKey=Username,AttributeValue="$P" --start-time "$DEBUT" --max-items 300 --query "Events[?contains(CloudTrailEvent, '\"readOnly\":false')].[EventTime,EventName,EventSource]" --output table
```

Résultat attendu : un tableau de vos actions, de la plus récente à la plus ancienne : `PutParameter`, `PutBucketPolicy`, `CreateBucket`, `RevokeSecurityGroupIngress`, `AuthorizeSecurityGroupIngress`, `CreateSecurityGroup`… Chaque modification de la veille est là, avec son heure exacte, y compris la correction (`RevokeSecurityGroupIngress`) qui a suivi l'erreur.

## Partie 2 — AWS : l'événement qui compte

Isolons **l'ouverture du port 22 au monde** et lisons l'événement complet. On en extrait les champs qu'un enquêteur regarde en premier.

```bash
# [AWS CloudShell]
export AWS_REGION=eu-west-3
P=$(aws sts get-caller-identity --query Arn --output text | awk -F/ '{print $NF}')
DEBUT=$(date -u -d "-2 days" +%Y-%m-%dT%H:%M:%SZ)
aws cloudtrail lookup-events --lookup-attributes AttributeKey=EventName,AttributeValue=AuthorizeSecurityGroupIngress --start-time "$DEBUT" --query "Events[?Username=='$P' && contains(CloudTrailEvent, '0.0.0.0/0')] | [0].CloudTrailEvent" --output text > evenement.json
if [ -s evenement.json ] && [ "$(cat evenement.json)" != "None" ]; then
  jq '{quand: .eventTime, qui: .userIdentity.arn, depuis_ip: .sourceIPAddress, outil: .userAgent, region: .awsRegion, action: .eventName, groupe: .requestParameters.groupId, regles: .requestParameters.ipPermissions}' evenement.json
  echo "OK : événement trouvé"
else
  echo "ERREUR : aucun AuthorizeSecurityGroupIngress de $P depuis 2 jours (refaites l'exercice 2, puis attendez 15 minutes)"
fi
```

Résultat attendu : un objet JSON qui dit **quand**, **qui** (votre ARN), **depuis quelle adresse IP**, **avec quel outil** (`userAgent` : CloudShell, console…) et **quelle règle** a été ajoutée (`0.0.0.0/0`, port 22).

## Partie 3 — AWS : qui d'autre ?

L'enquêteur élargit le champ : qui, dans tout le compte, a ouvert des règles de groupes de sécurité ces 2 derniers jours ?

```bash
# [AWS CloudShell]
export AWS_REGION=eu-west-3
DEBUT=$(date -u -d "-2 days" +%Y-%m-%dT%H:%M:%SZ)
aws cloudtrail lookup-events --lookup-attributes AttributeKey=EventName,AttributeValue=AuthorizeSecurityGroupIngress --start-time "$DEBUT" --query "Events[].Username" --output text | tr '\t' '\n' | sort | uniq -c | sort -rn
```

Résultat attendu : le nombre d'ouvertures de règles par utilisateur.

## Questions

1. D'après l'événement de la partie 2, depuis quelle adresse IP et avec quel outil avez-vous ouvert le port ? En quoi ces deux champs sont-ils précieux lors d'un incident réel ?
2. Vous voyez dans la partie 3 qu'un utilisateur a ouvert beaucoup de règles. Est-ce forcément un incident ? Que vérifiez-vous avant d'alerter ?

## Bonus Azure (facultatif) — le journal d'activité

Le **journal d'activité** (Activity Log) enregistre les opérations du **plan de contrôle** : créer, modifier, supprimer des ressources. Il garde **90 jours** d'historique. On écarte les évaluations automatiques des politiques Azure (`Microsoft.Authorization/policies/…`), très nombreuses, pour ne garder que vos actions.

```bash
# [Azure Cloud Shell]
U=$(az account show --query user.name -o tsv); N=${U%%@*}; RG=rg-${N//./-}
az monitor activity-log list -g "$RG" --offset 3d --query "[?caller=='$U' && status.value=='Succeeded' && !starts_with(operationName.value, 'Microsoft.Authorization/policies/')].{quand:eventTimestamp, operation:operationName.value}" -o table | head -n 40
```

Résultat attendu : vos opérations d'hier : `Microsoft.Network/networkSecurityGroups/securityRules/write`, `Microsoft.Storage/storageAccounts/write`, `Microsoft.Storage/storageAccounts/listKeys/action`… (celles de vos bonus Azure du jour 1).

Cherchez maintenant le **dépôt** du fichier `rapport.csv` dans votre compte de stockage (bonus de l'exercice 3) :

```bash
# [Azure Cloud Shell]
U=$(az account show --query user.name -o tsv); N=${U%%@*}; RG=rg-${N//./-}
NB=$(az monitor activity-log list -g "$RG" --offset 3d --query "length([?contains(operationName.value, 'secrets') || contains(operationName.value, 'blobs')])" -o tsv)
echo "Opérations sur des secrets ou des blobs trouvées dans le journal d'activité : $NB"
```

Résultat attendu : `0`. Le dépôt du fichier n'y figure pas.

Question du bonus : pourquoi le journal d'activité Azure ne contient-il ni la lecture d'un secret, ni le dépôt d'un fichier dans un stockage ? (Indice : **plan de contrôle** contre **plan de données**.)

<div style="page-break-before: always"></div>

# Exercice 5 — Réponse à incident : une clé a fuité

> Module : 15 — CL-SECU (version 2 jours) · Jour 2
> Durée estimée : 45 min
> Difficulté : 3 / 5
> Type : Exercice d'application (simulation d'incident)

## Objectifs pédagogiques

- Dérouler les étapes d'une réponse à incident : **identifier, contenir, enquêter, éradiquer**.
- **Contenir sans détruire** : désactiver plutôt que supprimer, pour garder les preuves.
- Vérifier que la mesure de confinement est **effective**.

## Contexte

Lundi, 9 h 12 : GitHub vous prévient qu'une **clé d'accès AWS** a été poussée dans un dépôt public. Des robots scannent GitHub en permanence : une clé publiée est utilisée en quelques minutes.

Pour s'entraîner sans danger, chacun **fabrique sa propre fuite** : un utilisateur IAM de test, sans aucun droit, et sa clé, qui sera « l'attaquant ».

## Partie 1 — Préparer la simulation (AWS)

```bash
# [AWS CloudShell]
export AWS_REGION=eu-west-3
P=$(aws sts get-caller-identity --query Arn --output text | awk -F/ '{print $NF}')
VICTIME="secu-$P-fuite"
aws iam get-user --user-name "$VICTIME" > /dev/null 2>&1 || aws iam create-user --user-name "$VICTIME" --tags Key=usage,Value=exercice-cl-secu > /dev/null
aws iam create-access-key --user-name "$VICTIME" > cle-fuitee.json
echo "Clé « fuitée » : $(jq -r .AccessKey.AccessKeyId cle-fuitee.json) (utilisateur $VICTIME, sans aucun droit)"
```

> Si vous relancez ce bloc, une **deuxième** clé est créée (2 au maximum par utilisateur). Le nettoyage de fin de module supprime l'utilisateur et toutes ses clés.

L'« attaquant » utilise la clé : il découvre à qui elle appartient, puis tente de lister les buckets du compte.

```bash
# [AWS CloudShell]
export AWS_REGION=eu-west-3
export AWS_ACCESS_KEY_ID=$(jq -r .AccessKey.AccessKeyId cle-fuitee.json)
export AWS_SECRET_ACCESS_KEY=$(jq -r .AccessKey.SecretAccessKey cle-fuitee.json)
unset AWS_SESSION_TOKEN
sleep 10
echo "--- L'attaquant : à qui appartient cette clé ? ---"
aws sts get-caller-identity --query Arn --output text
echo "--- L'attaquant : quels buckets ? ---"
aws s3 ls 2>&1 | head -n 3 || true
```

Résultat attendu : l'ARN de l'utilisateur `secu-…-fuite`, puis un `AccessDenied` sur `ListBuckets` : l'utilisateur n'a aucun droit… cette fois.

> ⚠️ Ce bloc **remplace** vos identifiants par ceux de la clé fuitée, et ce remplacement **reste actif** dans votre session CloudShell. C'est pourquoi tous les blocs AWS suivants commencent par `unset AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN` : cette ligne efface la clé fuitée et vous rend vos droits normaux. En cas de doute, fermez et rouvrez CloudShell.

## Partie 2 — Contenir (AWS)

**Contenir** = empêcher toute nouvelle utilisation, **sans détruire** les preuves. On **désactive** la clé (réversible) et on attache la politique `AWSDenyAll` à l'utilisateur, au cas où il aurait d'autres accès.

```bash
# [AWS CloudShell]
export AWS_REGION=eu-west-3
unset AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN
P=$(aws sts get-caller-identity --query Arn --output text | awk -F/ '{print $NF}')
VICTIME="secu-$P-fuite"
CLE=$(jq -r .AccessKey.AccessKeyId cle-fuitee.json)
aws iam update-access-key --user-name "$VICTIME" --access-key-id "$CLE" --status Inactive
aws iam attach-user-policy --user-name "$VICTIME" --policy-arn arn:aws:iam::aws:policy/AWSDenyAll
aws iam list-access-keys --user-name "$VICTIME" --query "AccessKeyMetadata[].{cle:AccessKeyId, statut:Status}" --output table
echo "Confinement appliqué à $(date +%H:%M:%S)"
```

Vérifiez que le confinement **fonctionne vraiment** : l'attaquant réessaie.

```bash
# [AWS CloudShell]
export AWS_REGION=eu-west-3
export AWS_ACCESS_KEY_ID=$(jq -r .AccessKey.AccessKeyId cle-fuitee.json)
export AWS_SECRET_ACCESS_KEY=$(jq -r .AccessKey.SecretAccessKey cle-fuitee.json)
unset AWS_SESSION_TOKEN
sleep 10
if aws sts get-caller-identity > /dev/null 2> erreur.txt; then echo "ERREUR : la clé fonctionne encore (attendez 30 s et relancez ce bloc)"; else echo "OK : la clé fuitée est refusée :"; cat erreur.txt; fi
```

Résultat attendu : `OK : la clé fuitée est refusée`, suivi d'une erreur `InvalidClientTokenId`.

## Partie 3 — Enquêter (AWS)

Qu'a fait la clé avant d'être coupée ? On interroge CloudTrail **par identifiant de clé**. Les événements apparaissent avec **5 à 15 minutes** de délai : si le tableau est vide, attendez et relancez.

```bash
# [AWS CloudShell]
export AWS_REGION=eu-west-3
unset AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN
CLE=$(jq -r .AccessKey.AccessKeyId cle-fuitee.json)
DEBUT=$(date -u -d "-1 day" +%Y-%m-%dT%H:%M:%SZ)
aws cloudtrail lookup-events --lookup-attributes AttributeKey=AccessKeyId,AttributeValue="$CLE" --start-time "$DEBUT" --query "Events[].{quand:EventTime, action:EventName, erreur:CloudTrailEvent}" --output json | jq -r '.[] | "\(.quand)  \(.action)  \((.erreur | fromjson | .errorCode) // "succès")  depuis \((.erreur | fromjson | .sourceIPAddress))"'
```

Résultat attendu (après le délai) : `GetCallerIdentity` réussi, `ListBuckets` en `AccessDenied`, avec l'adresse IP d'où venaient les appels.

## Questions

1. Pourquoi **désactiver** la clé plutôt que la **supprimer** tout de suite ? Quand la supprimer ?
2. Pourquoi attacher `AWSDenyAll` en plus de désactiver la clé ?
3. Quelle est la meilleure protection contre ce scénario : une meilleure surveillance, ou **ne pas avoir de clé longue durée du tout** ? Justifiez.

## Indices

<details>
<summary>Indice question 3</summary>

Rôles IAM pour les machines et les services, identités managées sur Azure, fédération OIDC pour les pipelines CI/CD : aucune clé longue durée à stocker, donc rien à faire fuiter.

</details>

## Bonus Azure (facultatif) — la clé du compte de stockage a fuité

Sur Azure, l'équivalent est la **clé d'accès d'un compte de stockage** : qui la détient lit et écrit **tout** le contenu du compte, sans aucun compte utilisateur. On simule la fuite de la clé `key1` du compte de stockage du bonus Azure de l'exercice 3 (faites ce bonus d'abord), puis on la **renouvelle** (*rotation*).

```bash
# [Azure Cloud Shell]
U=$(az account show --query user.name -o tsv); N=${U%%@*}; RG=rg-${N//./-}
ST=stsecu$(echo -n "$U" | md5sum | cut -c1-12)
FUITEE=$(az storage account keys list -n "$ST" -g "$RG" --query "[?keyName=='key1'].value" -o tsv)
echo "--- L'attaquant, avec la clé fuitée ---"
az storage blob list --account-name "$ST" --account-key "$FUITEE" -c donnees --query "[].name" -o tsv
echo "--- Contenir : rotation de key1 ---"
az storage account keys renew -n "$ST" -g "$RG" --key key1 -o none
sleep 15
echo "--- L'attaquant réessaie ---"
if az storage blob list --account-name "$ST" --account-key "$FUITEE" -c donnees -o none 2> erreur.txt; then echo "ERREUR : l'ancienne clé fonctionne encore (attendez 30 s et relancez ce bloc)"; else echo "OK : l'ancienne clé est refusée :"; head -n 2 erreur.txt; fi
```

Résultat attendu : le nom du fichier `rapport.csv` lu avec la clé fuitée, puis `OK : l'ancienne clé est refusée`, suivi d'une erreur d'authentification.

<div style="page-break-before: always"></div>

# Nettoyage de fin de module — ne rien laisser derrière soi

> Module : 15 — CL-SECU (version 2 jours) · Fin du jour 2
> Durée estimée : 10 min
> Type : Nettoyage obligatoire

## Objectif

Supprimer **tout** ce que vous avez créé pendant les deux jours, et **uniquement** ce que vous avez créé : chaque ressource visée porte votre nom. Le nettoyage fait partie du travail d'un administrateur cloud : une ressource oubliée coûte de l'argent et élargit la surface d'attaque.

## Partie 1 — AWS

Ce bloc supprime, s'ils existent : l'utilisateur IAM de test de l'exercice 5 et ses clés, le paramètre secret, le bucket et son contenu, et le groupe de sécurité. Chaque ligne ignore une ressource déjà absente : vous pouvez relancer le bloc sans risque.

```bash
# [AWS CloudShell]
unset AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN
export AWS_REGION=eu-west-3
P=$(aws sts get-caller-identity --query Arn --output text | awk -F/ '{print $NF}')
COMPTE=$(aws sts get-caller-identity --query Account --output text)
echo "Nettoyage des ressources de $P"
VICTIME="secu-$P-fuite"
if aws iam get-user --user-name "$VICTIME" > /dev/null 2>&1; then
  for cle in $(aws iam list-access-keys --user-name "$VICTIME" --query "AccessKeyMetadata[].AccessKeyId" --output text); do aws iam delete-access-key --user-name "$VICTIME" --access-key-id "$cle"; done
  aws iam detach-user-policy --user-name "$VICTIME" --policy-arn arn:aws:iam::aws:policy/AWSDenyAll 2> /dev/null || true
  aws iam delete-user --user-name "$VICTIME"
fi
aws ssm delete-parameter --name "/secu/$P/db-mot-de-passe" 2> /dev/null || true
BUCKET="secu-$P-$COMPTE"
if aws s3api head-bucket --bucket "$BUCKET" 2> /dev/null; then aws s3 rb "s3://$BUCKET" --force > /dev/null; fi
SG=$(aws ec2 describe-security-groups --filters Name=group-name,Values="secu-$P-sg" --query "SecurityGroups[0].GroupId" --output text)
if [ "$SG" != "None" ]; then aws ec2 delete-security-group --group-id "$SG"; fi
rm -f cle-fuitee.json
echo "Nettoyage AWS terminé"
```

Vérification :

```bash
# [AWS CloudShell]
unset AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN
export AWS_REGION=eu-west-3
P=$(aws sts get-caller-identity --query Arn --output text | awk -F/ '{print $NF}')
COMPTE=$(aws sts get-caller-identity --query Account --output text)
RESTE=0
aws iam get-user --user-name "secu-$P-fuite" > /dev/null 2>&1 && { echo "ERREUR : l'utilisateur secu-$P-fuite existe encore"; RESTE=1; }
aws ssm get-parameter --name "/secu/$P/db-mot-de-passe" > /dev/null 2>&1 && { echo "ERREUR : le paramètre secret existe encore"; RESTE=1; }
aws s3api head-bucket --bucket "secu-$P-$COMPTE" > /dev/null 2>&1 && { echo "ERREUR : le bucket existe encore"; RESTE=1; }
[ "$(aws ec2 describe-security-groups --filters Name=group-name,Values="secu-$P-sg" --query "length(SecurityGroups)" --output text)" != "0" ] && { echo "ERREUR : le groupe de sécurité existe encore"; RESTE=1; }
if [ "$RESTE" = "0" ]; then echo "OK : plus aucune ressource secu-$P sur AWS"; fi
```

## Partie 2 — Azure (seulement si vous avez fait des bonus Azure)

Ce bloc supprime le NSG et le compte de stockage des bonus, dans **votre** groupe de ressources. Le groupe de ressources lui-même est **conservé**.

```bash
# [Azure Cloud Shell]
U=$(az account show --query user.name -o tsv); N=${U%%@*}; RG=rg-${N//./-}
ST=stsecu$(echo -n "$U" | md5sum | cut -c1-12)
echo "Nettoyage des ressources des bonus dans $RG"
az network nsg delete -g "$RG" -n nsg-secu-audit -o none 2> /dev/null || true
az storage account delete -g "$RG" -n "$ST" --yes -o none 2> /dev/null || true
RESTE=$(az resource list -g "$RG" --query "length([?name=='nsg-secu-audit' || name=='$ST'])" -o tsv)
if [ "$RESTE" = "0" ]; then echo "OK : plus aucune ressource des bonus dans $RG"; else echo "ERREUR : $RESTE ressource(s) des bonus restent dans $RG (relancez ce bloc)"; fi
```

<div style="page-break-before: always"></div>

# Démo — Surveiller : l'audit express du compte et ce que voit GuardDuty

> Module : 15 — CL-SECU (version 2 jours) · Jour 2, début d'après-midi
> Durée live : 30 min (+ 20 min de discussion)
> Type : Démonstration formateur, rejouable par les stagiaires (tout est en **lecture seule**)

## Pitch (30 s)

« Depuis hier, vous avez corrigé des erreurs une par une. Un administrateur, lui, doit savoir **où en est tout le compte** : c'est le rôle des outils de *posture de sécurité* (CSPM). Et il doit savoir **ce qui se passe** : c'est le rôle d'un détecteur comme GuardDuty. Je vous montre les deux sur notre compte de formation. Vous allez voir que les robots d'Internet ne nous ont pas attendus. »

## Préparation avant la session

- [ ] Console AWS ouverte, région **Paris (eu-west-3)**, CloudShell ouvert. Un compte stagiaire suffit : tout est en lecture seule.
- [ ] Vérifier que GuardDuty est actif : `aws guardduty list-detectors --region eu-west-3` renvoie un identifiant.
- [ ] Terminal en police 16 pt minimum.

## Déroulé scripté

### Acte 1 — Ce que voit GuardDuty (10 min)

Ce qu'on dit :
> « GuardDuty analyse en continu les journaux du compte (appels d'API, requêtes DNS, flux réseau) et lève des alertes qualifiées. Regardons les dix dernières. »

```bash
# [AWS CloudShell]
export AWS_REGION=eu-west-3
DETECTEUR=$(aws guardduty list-detectors --query "DetectorIds[0]" --output text)
IDS=$(aws guardduty list-findings --detector-id "$DETECTEUR" --sort-criteria AttributeName=updatedAt,OrderBy=DESC --max-results 10 --no-paginate --query "FindingIds" --output text)
aws guardduty get-findings --detector-id "$DETECTEUR" --finding-ids $IDS --query "Findings[].{type:Type, gravite:Severity, titre:Title}" --output table
```

Résultat attendu à l'écran : de **vraies** alertes, typiquement `UnauthorizedAccess:EC2/SSHBruteForce` : « 42.101.43.119 is performing SSH brute force attacks against i-04f13… ».

Ce qu'on explique :

- des robots d'Internet tentent des mots de passe sur les instances de la promotion dont le **port 22 est ouvert au monde** : c'est exactement l'erreur de l'exercice 2, **mesurée** dans ce compte ;
- le **type** suit le format `Catégorie:Ressource/Comportement` ;
- la **gravité** va de 1 à 10 : une tentative de force brute (2) est fréquente ; une exfiltration de données (8) est grave.

### Acte 2 — L'audit express en 10 contrôles (15 min)

Ce qu'on dit :
> « Un auditeur ne clique pas : il **automatise** des contrôles, et chacun renvoie à une référence reconnue, ici le **CIS AWS Foundations Benchmark**. Ce script vérifie 10 points en lecture seule. »

```bash
# [AWS CloudShell]
unset AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN
cat > audit-express.sh <<'EOF'
#!/bin/bash
# Audit express de la posture de sécurité d'un compte AWS (lecture seule)
export AWS_REGION=eu-west-3
COMPTE=$(aws sts get-caller-identity --query Account --output text)
ligne() { printf "%-8s %-58s %-14s %s\n" "$1" "$2" "$3" "$4"; }
verdict() { if [ "$1" = "oui" ]; then echo "CONFORME"; else echo "NON CONFORME"; fi; }

ligne "CIS" "Contrôle" "Statut" "Mesure"
ligne "--------" "----------------------------------------------------------" "--------------" "-------------"

v=$(aws iam get-account-summary --query "SummaryMap.AccountMFAEnabled" --output text)
ligne "1.5" "MFA activée sur le compte root" "$(verdict $([ "$v" = "1" ] && echo oui))" "AccountMFAEnabled=$v"

v=$(aws iam get-account-summary --query "SummaryMap.AccountAccessKeysPresent" --output text)
ligne "1.4" "Aucune clé d'accès sur le compte root" "$(verdict $([ "$v" = "0" ] && echo oui))" "clés root=$v"

aws iam generate-credential-report > /dev/null 2>&1; sleep 5
aws iam get-credential-report --query Content --output text | base64 -d > rapport-iam.csv
v=$(awk -F, 'NR>1 && $4=="true" && $8=="false"' rapport-iam.csv | wc -l)
ligne "1.10" "Tous les utilisateurs console ont la MFA" "$(verdict $([ "$v" = "0" ] && echo oui))" "$v sans MFA"

v=$(aws iam get-account-password-policy --query "PasswordPolicy.MinimumPasswordLength" --output text 2> /dev/null || echo 0)
ligne "1.8" "Mots de passe d'au moins 14 caractères" "$(verdict $([ "$v" -ge 14 ] && echo oui))" "minimum=$v"

v=$(aws accessanalyzer list-analyzers --query "length(analyzers)" --output text)
ligne "1.20" "IAM Access Analyzer activé" "$(verdict $([ "$v" -ge 1 ] && echo oui))" "$v analyseur(s)"

v=$(aws cloudtrail describe-trails --query "length(trailList[?IsMultiRegionTrail])" --output text)
ligne "3.1" "Un trail CloudTrail multi-régions existe" "$(verdict $([ "$v" -ge 1 ] && echo oui))" "$v trail(s)"

v=$(aws s3control get-public-access-block --account-id "$COMPTE" --query "PublicAccessBlockConfiguration.BlockPublicPolicy" --output text 2> /dev/null || echo absent)
ligne "2.1.4" "Blocage de l'accès public S3 au niveau du compte" "$(verdict $([ "$v" = "True" ] && echo oui))" "BlockPublicPolicy=$v"

v=$(aws ec2 get-ebs-encryption-by-default --query EbsEncryptionByDefault --output text)
ligne "2.2.1" "Chiffrement EBS par défaut (région)" "$(verdict $([ "$v" = "True" ] && echo oui))" "par défaut=$v"

v=$(aws ec2 describe-security-groups --filters Name=ip-permission.from-port,Values=22 Name=ip-permission.cidr,Values=0.0.0.0/0 --query "length(SecurityGroups)" --output text)
ligne "5.2" "Aucun groupe n'ouvre SSH (22) à tout Internet" "$(verdict $([ "$v" = "0" ] && echo oui))" "$v groupe(s)"

v=$(aws guardduty list-detectors --query "length(DetectorIds)" --output text)
ligne "-" "GuardDuty (détection des menaces) activé" "$(verdict $([ "$v" -ge 1 ] && echo oui))" "$v détecteur(s)"
EOF
chmod +x audit-express.sh
./audit-express.sh | tee resultat-audit.txt
echo "---"
echo "Contrôles conformes : $(grep -v 'NON CONFORME' resultat-audit.txt | grep -c 'CONFORME') / 10"
```

Résultat attendu : un tableau de 10 contrôles, avec un score d'environ **2 ou 3 sur 10**. Le score du compte de formation n'est pas bon : c'est normal, et c'est tout l'intérêt de la démo.

Pour un constat, l'auditeur produit la **liste** des éléments concernés, et pas seulement un nombre :

```bash
# [AWS CloudShell]
unset AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN
echo "--- Utilisateurs avec mot de passe console mais SANS MFA ---"
awk -F, 'NR>1 && $4=="true" && $8=="false" {print $1 "  (dernière connexion : " $5 ")"}' rapport-iam.csv
echo "--- Clés d'accès actives, avec leur dernière rotation ---"
awk -F, 'NR>1 && $9=="true" {print $1 "  clé 1 créée le " $10 ", dernière utilisation " $11}' rapport-iam.csv | head -n 15
```

Ce qu'on explique :

- **1.10** : un compte console sans MFA ne tient qu'à son mot de passe ;
- **5.2** : le port 22 ouvert, encore lui ;
- **2.1.4** : le blocage de l'accès public S3 **au niveau du compte** protégerait tous les buckets d'un coup ; un stagiaire **ne doit pas** l'activer lui-même, car c'est une décision du propriétaire du compte ;
- **3.1** : sans **trail** CloudTrail, les événements ne sont conservés que 90 jours et ne peuvent pas déclencher d'alerte automatique.

### Acte 3 — Discussion : le rapport d'audit (20 min)

Par binômes, les stagiaires rédigent en 10 minutes, pour le responsable du compte :

1. le score global ;
2. les **3 constats prioritaires**, chacun avec le risque concret en une phrase, la correction recommandée et l'effort estimé (faible, moyen, élevé) ;
3. un constat **acceptable** dans le contexte d'une formation, et pourquoi.

Mise en commun : comparer les priorités des binômes. Il n'y a pas une seule bonne réponse, mais des **justifications** plus ou moins solides.

### Conclusion (2 min)

Message clé :
> « On ne sécurise bien que ce qu'on mesure. Un script d'audit, c'est une mesure **reproductible** : on le relance après correction, et le score doit monter. Des outils comme AWS Security Hub, Prowler ou Microsoft Defender for Cloud font la même chose, avec des centaines de contrôles. »

## Plan B

| Problème | Plan B |
|---|---|
| `generate-credential-report` met du temps | Relancer le bloc de l'acte 2 : le rapport est prêt au deuxième passage |
| GuardDuty n'a aucune alerte récente | Montrer la console GuardDuty, ou générer des exemples : `aws guardduty create-sample-findings --region eu-west-3 --detector-id "$(aws guardduty list-detectors --region eu-west-3 --query 'DetectorIds[0]' --output text)" --finding-types "Recon:IAMUser/MaliciousIPCaller.Custom"` |

## Points d'attention

- La liste des utilisateurs sans MFA affiche des comptes de **salariés**. C'est une donnée d'audit légitime, à commenter avec tact.
- Le contrôle **1.4** (clé d'accès sur le compte root) est **sensible** : s'il est non conforme, ne pas le commenter en séance ; le traiter avec le propriétaire du compte.
