# Camera Controller

## 🇬🇧 English 🇬🇧

### Introduction

Hello ! You can find here the Python script I have made to make your camera into a controller.
For now, it's a simple script but in the future I would love to make a more concrete program with better features.
As I have few projects in my portfolio, be indulgent to me and don't hesitate to make some comments on how I can make this project a better one.

### How does it work

This script will switch on your default camera, and create a grid with several inputs. When you have your face inside one of the input square, the input will be made on your keyboard.
As I am currently into GameBoy games, I mapped it by default to a GameBoy Advance setup.

It uses the Google [MediaPipe](https://ai.google.dev/edge/mediapipe/solutions/guide) library with its facial recognition model to detect your face and its position in the said grid.

Every steps are detailed inside the script if you are curious.

### Installation

#### Prerequisites

Please install [Python](https://www.python.org/) with pip on your machine if you have not already done so (I personally have version 3.11). If you have the direct link I may have given you, you just need to download the executable.

#### The steps

1 - First, pull the code to have it on your computer.

2 - Install all dependencies by running this command line within the local repository clone:

![image](https://github.com/user-attachments/assets/38f07881-8f6d-42bd-b9dc-c9903b3e97d0)

3 - In the main.py file, edit the keys you want to set by modifying the array possible_inputs.

**Important note**: each number next to the keys corresponds to the virtual key number (e.g. 103 is key 7 on the numeric keypad, 104 is key 8, etc.). To choose the keys you want, you can find [here](https://cherrytree.at/misc/vk.htm) the list of virtual key numbers.

4 - Once you've done this, run the script with the python3 command main.py or via VSCode.

## 🇫🇷 Français 🇫🇷

### Introduction

Bonjour ! Vous pouvez retrouver ici le script que j'ai conçu permettant de transformer votre Webcam en une manette.
Pour le moment c'est un simple script mais dans le futur je serai ravi d'en faire un programme concret avec des meilleurs optionnalités.
Comme j'ai peu de projets dans mon portfolio, soyez indulgents, mais n'hésitez pas à faire des critiques constructives pour que je m'améliore.

### Comment ça fonctionne

Ce script va allumer votre caméra par défaut, et créer une grille avec plusieurs touches. Quand vous aurez votre visage reconnu dans l'une des cases de la grille, la touche associée va être virtuellement appuyé sur votre clavier.
Comme je suis à fond sur des jeux de GameBoy Advance récemment, j'ai décidé de mapper les touches de manière à pouvoir jouer à la GameBoy avec ma tête ou mes mains.

Cela utilise la librairie [MediaPipe](https://ai.google.dev/edge/mediapipe/solutions/guide) de Google avec son modèle de reconnaissance faciale pour détecter votre visage dans la grille.

Chaque étape est décrite dans le script (attention aux non-anglophones, les commentaires sont en anglais 😉).


### Installation

#### Prérequis

Veuillez installer [Python](https://www.python.org/) avec pip sur votre machine si ce n'est pas déjà fait. (J'ai la version 3.11 personnellement). Si vous avez juste le lien que je vous ai peut-être donné, veuillez juste télécharger l'exécutable.

#### Les étapes

1 - En premier lieu, veuillez pull le code pour l'avoir sur votre ordinateur
2 - Installez toutes les dépendances en exécutant cette ligne de commande au sein du clone local du repository :

![image](https://github.com/user-attachments/assets/38f07881-8f6d-42bd-b9dc-c9903b3e97d0)

3 - Sur le fichier main.py, éditez les touches que vous voulez mettre en modifiant l'array possible_inputs.

**Note importante** : chaque numéro a coté des touches correspondent au numéro de touche virtuel (par exemple 103 est la touche 7 du pavé numérique, 104 est la touche 8, etc...). Pour choisir les touches que vous voulez, vous pouvez retrouver [ici](https://cherrytree.at/misc/vk.htm) la liste des numéros de touche virtuelle.

4 - Une fois cela fait, lancez le script en faisant la commande python3 main.py ou bien via VSCode.




## How it looks like / Voici le rendu

![image](https://github.com/user-attachments/assets/b3fa6303-8219-47c9-b81d-4c340876e345)
