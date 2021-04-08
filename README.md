# Nabaztag en Python pour Raspberry Pi

[![Build Status](https://travis-ci.org/thelemax/pynab.svg?branch=master)](https://travis-ci.org/thelemax/pynab)
![Tests](https://github.com/thelemax/pynab/workflows/Tests/badge.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/thelemax/pynab.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/thelemax/pynab/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/thelemax/pynab.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/thelemax/pynab/context:python)
[![codecov](https://codecov.io/gh/thelemax/pynab/branch/master/graph/badge.svg)](https://codecov.io/gh/thelemax/pynab)

# Cartes

Ce système est conçu pour le Nabaztag v1. Ce projet est un fork de nabaztag2018/pynab et a vocation uniquement de refaire fonctionner un Nabaztag v1 avec un minimum de composant nécessaire. Toutes les fonctionnalités qu'offre le projet de base ne seront pas en place, notamment la gestion de position des oreille.

Les schémas et fichiers de fabrication son à venir.

# Images

Les [releases](https://github.com/nabaztag2018/pynab/releases) sont des images de Raspbian Buster Lite 2019-09-26 avec pynab pré-installé. Elles ont les mêmes réglages que [Raspbian](https://www.raspberrypi.org/downloads/raspbian/).

Les releases actuelles (0.7.x) ne fonctionnent que sur les cartes 2019 (cf #44)

# Installation sur Raspbian (pour développeurs !)

0. S'assurer que le système est bien à jour

Le script d'installation requiert désormais une Raspbian avec buster, pour bénéficier de Python 3.7.
Il est nécessaire que les headers depuis le paquet apt correspondent à la version du noyau.

```
sudo apt update
sudo apt upgrade
```

1. Configurer la carte son.

https://github.com/pguyot/wm8960/tree/tagtagtag-sound


2. Installer PostgreSQL et les paquets requis

```
sudo apt-get install postgresql libpq-dev git python3 python3-venv python3-dev gettext nginx openssl libssl-dev libffi-dev libmpg123-dev libasound2-dev libatlas-base-dev libgfortran3 libopenblas-dev liblapack-dev gfortran
```

3. Récupérer le code

```
git clone https://github.com/thelemax/pynab.git
cd pynab
```

4. Lancer le script d'installation qui fait le reste, notamment l'installation et le démarrage des services via systemd.

```
bash install.sh
```

# Mise à jour

A priori, cela fonctionne via l'interface web.
Si nécessaire, il est possible de le faire en ligne de commande avec :
```
cd pynab
bash upgrade.sh
``` 

# Nabblockly

[Nabblockly](https://github.com/pguyot/nabblockly), une interface de programmation des chorégraphies du lapin par blocs, est installé sur les images des releases depuis la 0.6.3b et fonctionne sur le port 8080. L'installation est possible sur le port 80 en modifiant la configuration de Nginx.

# Architecture

Cf le document [PROTOCOL.md](PROTOCOL.md)

- nabd : daemon qui gère le lapin (i/o, chorégraphies)
- nab8balld : daemon pour le service gourou
- nabairqualityd : daemon pour le service de qualité de l'air
- nabclockd : daemon pour le service horloge
- nabsurprised : daemon pour le service surprises
- nabtaichid : daemon pour le service taichi
- nabmastodond : daemon pour le service mastodon
- nabweatherd : daemon pour le service météo
- nabweb : interface web pour la configuration
