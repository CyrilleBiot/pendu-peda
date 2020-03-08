# pendu-peda
Jeu du pendu avec comme thèmes les domaines d'apprentissages des cycles 2 et 3 de l'école primaire.

Hangman game with as themes the learning areas of cycles 2 and 3 of primary school. Pendu-peda does not take any options. Thematic files can be incremented in the directory : usr/share/pendu-peda/data-files/

## WARNING
Version obsolète, abandonnée au profit d'un développement basé sur GTK plutôt que TK
Nouvelle version disponible :
<a href="https://github.com/CyrilleBiot/pendu-peda-gtk">https://github.com/CyrilleBiot/pendu-peda-gtk</a>


## Build your package

```
$ git clone https://github.com/CyrilleBiot/pendu-peda.git
$ cd pendu-peda
$ debuild -us -uc
```

## Info
Premier jet. Livré brut. Sans debug mais fonctionnel.
Les nouveaux de conf sont à mettre dans :
 usr/share/pendu-peda/data-files/

## TODO
Retravailler l'interface
Mettre un repertoire data dans le dossier de l'$user
Griser les lettres déjà utiliser
Passer le tout en gtk


