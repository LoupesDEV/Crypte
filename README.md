<div align="center">
    <img src="medias/README/header.png">
</div>

<h1 align="center">CRYPTE</h1>

<div align="center">
    <p>Application desktop Python pour stocker des mots de passe de maniere chiffree, les rechercher rapidement et les modifier facilement.</p>
    <img src="https://m3-markdown-badges.vercel.app/stars/9/3/LoupesDEV/Crypte">
    <img src="https://ziadoua.github.io/m3-Markdown-Badges/badges/Python/python3.svg">
</div>

<br>

## Table des matieres

- [Technologies utilisees](#technologies-utilisees)
- [Prerequis & compatibilite](#prerequis--compatibilite)
- [Installation](#installation)
- [Lancement](#lancement)
- [Fonctionnalites](#fonctionnalites)
- [Format des donnees](#format-des-donnees)
- [Structure du projet](#structure-du-projet)
- [Securite & limites](#securite--limites)
- [Roadmap](#roadmap)
- [FAQ](#faq)

## Technologies utilisees

Crypte est construit avec une stack simple, locale et sans service externe :

- **Python 3** : langage principal de l'application
- **Tkinter / ttk** : interface graphique desktop
- **cryptography (Fernet)** : chiffrement symetrique des entrees
- **JSON** : serialisation des donnees par entree
- **SHA-256 + Base64 URL-safe** : derivation de cle depuis le master password

## Prerequis & compatibilite

### Environnement requis

- **Python** : 3.10+
- **OS** : macOS, Linux, Windows
- **Pip** : pour installer les dependances

### Dependances Python

Le fichier `requirements.txt` contient :

```txt
cryptography>=42.0.0
```

## Installation

1. **Cloner le depot**

```bash
git clone https://github.com/LoupesDEV/Crypte.git
cd Crypte
```

2. **Creer un environnement virtuel (recommande)**

macOS / Linux :

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows (PowerShell) :

```powershell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
```

3. **Installer les dependances**

```bash
pip install -r requirements.txt
```

## Lancement

Tu as 3 facons de lancer l'application :

- **Script shell (macOS/Linux)**

```bash
./run.sh
```

- **Script batch (Windows)**

```bat
run.bat
```

- **Execution directe Python**

```bash
python main.py
```

## Fonctionnalites

### Gestion des mots de passe

- Ajout d'une entree : `site`, `utilisateur`, `mot de passe`, `note`
- Edition d'une entree par double-clic sur une ligne
- Suppression de l'entree selectionnee
- Affichage masque du mot de passe (points) avec reveal/hide

### Productivite

- Copie rapide du **nom d'utilisateur** et du **mot de passe** dans le presse-papiers
- Barre de recherche instantanee par **site**
- Interface moderne avec tableau, alternance de lignes et panneau lateral

### Securite locale

- Demande d'un **master password** au demarrage
- Verification du mot de passe maitre avant chargement des donnees
- Chiffrement Fernet ligne par ligne dans `vault/crypte.dat`

### UX

- Fenetres popup dediees pour ajouter/modifier
- Bouton `Quitter` en bas de la colonne gauche
- Icone de fenetre chargee depuis `assets/logo.png` (si disponible)

## Format des donnees

Les donnees sont stockees dans `vault/crypte.dat`.

Chaque ligne du fichier contient une entree chiffree. Une fois dechiffree, la structure JSON est :

```json
{
	"site": "github.com",
	"user": "mon_utilisateur",
	"password": "mon_mot_de_passe",
	"note": "2FA active"
}
```

## Structure du projet

```md
Crypte/
├── main.py                # Point d'entree de l'application
├── requirements.txt       # Dependances Python
├── run.sh                 # Lancement macOS/Linux
├── run.bat                # Lancement Windows
├── README.md              # Documentation
├── assets/
│   ├── logo.png           # Icone principale utilisee par l'app
│   └── logo_nobg.png      # Variante de logo
├── vault/
│   └── crypte.dat         # Base de donnees chiffree (une entree par ligne)
└── crypte/
    ├── __init__.py        # Export de la classe principale
    ├── app.py             # UI + logique applicative
    ├── constants.py       # Couleurs et constantes d'interface
    ├── styles.py          # Styles ttk
    ├── security.py        # Derivation de cle + verification decrypt
    └── storage.py         # Lecture/ecriture chiffree des entrees
```

## Securite & limites

### Ce que le projet fait bien

- Chiffrement local des donnees avec Fernet
- Aucune base distante ni API externe
- Donnees chargees uniquement si le master password est correct

### Limites actuelles

- Derivation de cle basee sur SHA-256 simple (sans sel ni KDF avance type PBKDF2/Argon2)
- Pas de rotation de cle
- Pas de verrouillage automatique apres inactivite
- Pas d'historique/versionning des entrees

## Roadmap

- [ ] Tri des entrees (A-Z, date de creation, etc.)
- [ ] Export/import chiffre
- [ ] KDF renforce (PBKDF2 ou Argon2)

## FAQ

### Le fichier `vault/crypte.dat` n'existe pas au premier lancement, est-ce normal ?

Oui. Le fichier est cree automatiquement quand tu enregistres la premiere entree.

### J'ai oublie mon master password, je peux recuperer les donnees ?

Non. Sans le master password correct, le dechiffrement est impossible.

### Pourquoi les mots de passe sont affiches en points ?

Par securite visuelle. Utilise le bouton `Reveal/Hide mdp` pour basculer l'affichage.

### Comment contribuer ?

Tu peux ouvrir une issue ou proposer une pull request sur le depot GitHub.
