# Sudoku AI

## Auteur

- [Alexandre Jeunot-Caire](https://github.com/jeunotca)


## Visuel

<img src="./thumbnail.png" alt="Rendu de l'algorithme sur une grille" style="margin: auto;"/>

## Description

Programme <b>personnel</b> développé en `Python` de scanner une grille de Sudoku et de la résoudre, avant d'afficher la réponse aux cases manquantes sur la grille.


### Implémentation

Le programme a été développé en `Python` en utilisant principalement les bibliothèques `opencv` (cv2) et `numpy` pour le traitement d'image. La reconnaissance des chiffres est effectuée à l'aide de `Keras / Tensorflow` sur un modèle entraîné sur un dataset custom de **44 321** images issues d'un premier livre de Sudoku.

Les images présentes dans `test` sont issues d'un second livre de Sudoku qui n'a pas participé à l'élaboration du dataset.

## Installation

### Récupération des sources

* Depuis l'invité de commandes (HTTP):
```bash
$ git clone https://github.com/jeunotca/sudoku-solver-ai.git
$ cd sudoku-solver-ai
```

**OU**

* Depuis l'invité de commandes (SSH):
```bash
$ git clone git@github.com:jeunotca/sudoku-solver-ai.git
$ cd sudoku-solver-ai
```

**OU**

* En téléchargeant les sources puis en extrayant l'archive

### Installation

```bash
$ pip install -r requirements.txt
```

**OU**

* En téléchargeant les sources puis en extrayant l'archive

## Utilisation

### Exécution du projet

```bash
$ python3 main.py
```

Dans cette situation, l'algorithme traitera l'image définie dans `default.py`. Sinon, il est également possible de choisir une image en utilisant

```bash
$ python3 main.py -i chemin/de/l/image.jpg
```

Dans les deux cas, la solution sera enregistrée au même endroit que l'image d'origine au format `nom-image-d-origine-result.jpg`.

## AI

* L'IA utilisée est la suivante :
  * Fully connected de 784
  * Conv2D 32 filtres, kernel de 3, stride de 1, fonction ReLU
  * Batch normalization
  * Conv2D 32 filtres, kernel de 3, stride de 1, fonction ReLU
  * Batch normalization
  * Conv2D 32 filtres, kernel de 5, stride de 1, fonction ReLU
  * Batch normalization
  * Dropout de 0.4
  * Conv2D 64 filtres, kernel de 3, stride de 1, fonction ReLU
  * Batch normalization
  * Conv2D 64 filtres, kernel de 3, stride de 1, fonction ReLU
  * Batch normalization
  * Conv2D 64 filtres, kernel de 5, stride de 1, fonction ReLU
  * Batch normalization
  * Dropout de 0.4
  * Fully connected de 128, fonction ReLU
  * Dropout de 0.3
  * Fully connected de 128, fonction ReLU
  * Dropout de 0.4
  * Fully connected de 10, fonction softmax

Optimizeur Adam de learning rate = 1e-4 et loss function `Sparse categorical crossentropy`

Ce modèle a été réalisé en collaboration avec **Michael Gellenoncourt**.

L'IA a un taux de réussite de `99.78%` sur nos tests.

### Dossier AI

Le dossier AI contient le modèle que nous avons utilisé, ainsi que des fonctions permettant si vous le souhaitez de créer vos propres modèles à l'aide des images situées dans le dossier `dataset/raw`.
 