# Déploiement

## Ajouter une nouvelle instance

- dans le fichier `hosts`, ajouter les entrées
- dans le fichier `settings.ini.j2`, mettre à jour la partie "localization"
- mettre à jour les fichiers regions.py, departements.py, epci.py et communes.py
- lancer `ansible-playbook backend.yml -l [instance]`
- copier la BDD, depuis un shell `psql`
    - `DROP DATABASE demometre_belgique_preprod;`
    - `CREATE DATABASE demometre_belgique_preprod WITH TEMPLATE "do" owner demometre_belgique_preprod;`
    - `REASSIGN OWNED BY "do" to demometre_belgique_preprod ;`
    - `\c demometre_belgique_preprod`
    - supprimer le contenu des tables

```
delete from open_democracy_back_zipcode CASCADE;
delete from open_democracy_back_municipalityorderbyepci CASCADE;
delete from open_democracy_back_participation_profiles CASCADE;
delete from open_democracy_back_participationpillarcompleted CASCADE;
delete from open_democracy_back_participationresponse_multiple_choice_r90f4 CASCADE;
delete from open_democracy_back_closedwithscalecategoryresponse CASCADE;
delete from open_democracy_back_participationresponse CASCADE;
delete from open_democracy_back_participation CASCADE;
delete from open_democracy_back_assessmentrepresentativity CASCADE;
delete from open_democracy_back_assessmentresponse_multiple_choice_response CASCADE;
delete from open_democracy_back_assessmentresponse CASCADE;
delete from open_democracy_back_workshop CASCADE;
delete from open_democracy_back_assessment_experts CASCADE;
delete from open_democracy_back_assessment CASCADE;
delete from open_democracy_back_epci CASCADE;
delete from open_democracy_back_municipality CASCADE;
delete from open_democracy_back_department CASCADE;
delete from open_democracy_back_region CASCADE;
delete from my_auth_userresetkey CASCADE;
delete from my_auth_user_groups CASCADE;
delete from my_auth_user CASCADE;
```
- créer un utilisateur superuser : `sudo demometre_belgique_preprod-ctl createsuperuser`
- lancer le playbook front : `ansible-playbook frontend -l [instance]`
- importer les localités : `sudo demometre_belgique_prod-ctl import_political_division`
