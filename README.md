# Fusion de PDFs

Ce programme Python permet de fusionner des pages d'un PDF source avec d'autres fichiers PDF basés sur un motif spécifique. Le motif est déterminé en fonction de certaines données extraites des pages du PDF source.

## Prérequis

Avant d'exécuter ce programme, vous devez avoir installé Python ainsi que les bibliothèques nécessaires. Suivez les étapes ci-dessous pour préparer votre environnement.

### Installation de Python

1. **Télécharger Python :**
   - Allez sur le site officiel de [Python](https://www.python.org/downloads/).
   - Téléchargez la dernière version de Python compatible avec votre système d'exploitation (Windows, macOS, ou Linux).

2. **Installer Python :**
   - Lancez le fichier d'installation téléchargé.
   - Assurez-vous de cocher la case "Add Python to PATH" avant de cliquer sur "Install Now".

### Installation des Bibliothèques Nécessaires

Le programme utilise les bibliothèques suivantes :
- `os` (préinstallé avec python)
- `glob` (préinstallé avec python)
- `re` (préinstallé avec python)
- `pymupdf` (non installé avec python)

Pour installer la bibliothèque `pymupdf` , vous devez utiliser `pip`, l'outil de gestion de paquets de Python. Ouvrez une fenêtre de terminal ou une invite de commandes et exécutez les commandes suivantes :

```sh
pip install pymupdf
```

#### Configuration du Programme

Avant d'exécuter le programme, vous devez configurer certains chemins dans le script. Modifiez les variables suivantes selon vos besoins :

- **SOURCE_DATA_FILE** : Chemin complet vers le fichier PDF source à partir duquel les données seront extraites.
- **PATH_SEARCH** : Chemin vers le dossier où les fichiers PDF à rechercher sont stockés.
- **MERGED_PDF_DIRECTORY** : Chemin vers le dossier où les fichiers PDF fusionnés seront enregistrés.
- **TYPE** : Type d'opération, soit `"C"` pour "chéque" soit `"V"` pour "virement".

##### Utilisation

Placez tous les fichiers nécessaires dans les répertoires appropriés :

- Le fichier PDF source dans le chemin spécifié par `SOURCE_DATA_FILE`.
- Les fichiers PDF à rechercher dans le dossier spécifié par `PATH_SEARCH`.

Exécutez le script Python :

1. Ouvrez une fenêtre de terminal ou une invite de commandes.
2. Naviguez jusqu'au répertoire contenant votre script Python.
3. Exécutez le script avec la commande suivante :

   ```sh
   python app.py
