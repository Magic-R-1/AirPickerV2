# AirPickerV2

# TODO
Gestion des dates, les convertir et les mettre en date en base

# Aide avec PostgreSQL
brew services list
brew services stop postgresql
brew services start postgresql

# Masquage des fichiers __init__.py
IntelliJ IDEA
Settings
Editor
File Types
Ignored Files and Folders

__init__.py
venv
.idea

# Niveau de log globaux et de SQLAlchemy
CRITICAL (50) : Utilisé pour les messages les plus graves qui indiquent des erreurs fatales.
ERROR (40) : Utilisé pour des erreurs qui nécessitent une attention immédiate mais qui n'arrêtent pas le programme.
WARNING (30) : Indique une situation qui pourrait devenir un problème ou une exception potentielle.
INFO (20) : Messages informatifs sur le fonctionnement normal de l'application (souvent utilisés pour des informations générales sur les processus).
DEBUG (10) : Fournit des informations détaillées sur le flux d'exécution pour déboguer le programme. Ce niveau affiche une grande quantité de détails.
NOTSET (0) : Le niveau le plus bas, affichant absolument tout. Ce niveau est généralement utilisé pour ne pas filtrer du tout les messages de log.

# Organisation des couches de développement
1 - models : couche chargée de répliquer ce qui est en BDD
2 - schemas : couche chargée de sérialiser l'objet model récupéré
3 - dto : couche chargée de contenir les attributs absents de la base, tels que toutes les mesures du tableau d'impact
4 - services : couche chargée de contenir les méthodes utilisées pour calculer les mesures du tableau d'impact
