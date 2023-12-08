# Resawod_nubapp

EN/US at the bottom

## Description

Resawod_nubapp est un script permettant de réserver automatiquement les créneaux d'une structure utilisant la plateforme Resawod.

## Usage

### Installation

- pip3 install -r requirements.txt
- faire une copie du fichier personnal_data/users.json.example / le renommer en users.json puis remplacer les valeurs par celles des utilisateurs et des slots à réserver

### Lancement

- ./book.py 
- python3 book.py

#### Arguments

- h : affiche l'aide
- m : mode multi-utilisateur (facultatif) (conseillé) : va réserver les créneaux pour tous les utilisateurs en fonction des slots définis dans le fichier users.json
- u : utilisateur à utiliser (obligatoire) en mode mono-utilisateur
- p : mot de passe à utiliser (obligatoire) en mode mono-utilisateur

## À venir

- [X] Ajout d'un mode dev pour tester le script sans réserver de créneaux
- [X] Ajout d'un mode multi-utilisateur
- [ ] Ajout d'un mode first connexion pour afficher l'id des créneaux
- [ ] Ajout d'un check de la publication du nouveau planning le dimanche soir pour lancer la réservation des créneaux de la semaine suivante
- [ ] Ajout d'un mode multi créneaux sur une même journée
