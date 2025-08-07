# Déploiement

## Ajouter une nouvelle instance

- dans le fichier `hosts`, ajouter les entrées
- dans le fichier `settings.ini.j2`, mettre à jour la partie "localization"
- mettre à jour les fichiers regions.py, departements.py, epci.py et communes.py
- copier la BDD, depuis un shell `psql`
    - `CREATE DATABASE demometre_belgique_preprod WITH TEMPLATE "do" owner demometre_belgique_preprod;`
    - supprimer le contenu des tables

```
open_democracy_back_zipcode
open_democracy_back_municipality
open_democracy_back_municipalityorderbyepci
open_democracy_back_participation_profiles
open_democracy_back_participationpillarcompleted
open_democracy_back_participationresponse_multiple_choice_r90f4
open_democracy_back_closedwithscalecategoryresponse
open_democracy_back_participation
open_democracy_back_assessmentrepresentativity
open_democracy_back_assessmentresponse_multiple_choice_response
open_democracy_back_assessmentresponse
open_democracy_back_workshop
open_democracy_back_assessment_experts
open_democracy_back_assessment
open_democracy_back_epci
open_democracy_back_municipality
open_democracy_back_department
open_democracy_back_region
my_auth_userresetkey
my_auth_user_groups
my_auth_user
```
- créer un utilisateur superuser : `sudo demometre_belgique_preprod-ctl createsuperuser`

- lancer les playbooks
    - ansible-playbook backend.yml -l [instance]
    - ansible-playbook frontend -l [instance]
