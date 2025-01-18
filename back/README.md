# Site de Démocratie Ouverte

## Vocabulaire

- Assessment : une évaluation, il y en a une par ville. Elles peuvent être de trois
types (AssessmentType) : Diagnostic rapide, Evaluation participative, Evaluation avec
expert
- Participation : une participation d'un utilisateur à une évaluation. Toutes les
réponses sont liées à une participation.
- ParticipationResponse : la réponse d'un utilisateur à une question. Comprend donc un
couple (réponse, participation).
- AssessmentResponse : une réponse à une question objective, qui est donc unique pour
une évaluation
- Question, Response : Question, Réponse, qui sont les questions du questionnaires et
les réponses possibles pour chaque question
  - une Question a un booléen `profiling_question` pour indiquer si c'est une question
  de profilage
  - QuestionnaireQuestion : ??
  - ProfilingQuestion : pourquoi à la fois ce modèle là et le booléen
  `profiling_question` ?
  - ResponseChoice : une réponse possible à une question
- Score : `associated_score` (pour l'affichage) entre 1 et 4 et `linearized_score`
(pour le calcul) entre 0 et 1.

## Configuration du site

La configuration se fait depuis l'interface d'aministration, accessible à l'adresse :
`/admin/`.

### Pages

### Questions
Les questions ne sont pas configurés comme des pages

### Partie expert
Afin de pouvoir la tester il y a plusieurs étapes (en effet seulement les experts associés à une évaluation doivent pouvoir avoir accès à cette partie là):
- Dans le backoffice : Paramètres > Utilisateurs > Rechercher l'utilisateur que l'on veut déclarer en tant qu'expert. Aller dans l'onglet Rôles et sélectionner la case Experts puis enregistrer. La personne est alors enregistrée comme étant un expert

![](readme-images/expert-role.png)

- Dans le backoffice: Evaluations > Evaluation > Selectionner l'évaluation pour laquelle vous souhaitez ajouter un expert > Indiquez que c'est une évaluation avec experts + Selectionner l'expert dans la liste + indiquer que la redevance a été payée (sinon l'expert n'aura pas accès à cette évaluation) (NB : depuis le parcours utilisateur de la plateforme il est possible d'ajouter un expert, cependant il est possible de déclarer que la redevance a été payée seulement depuis l'admin wagtail)

![](readme-images/assessment-experts.png)

Pour terminer : connectez-vous à la plateforme du DémoMètre avec le compte que vous avez déclaré comme étant expert, depuis la page du profile il y aura un bouton qui permet d'accéder à l'espace expert "Espace animateur".

## Pour les développeurs

### Ajouter une langue

- ajouter la langue dans `settings/base.py`, dans les `WAGTAIL_CONTENT_LANGUAGES` et
`LOCALES_FOR_TRANSLATED_FIELDS`
- ajouter manuellement le champ Criteria.explanatory_{locale}
- lancer `python manage.py makemigrations` (des champs sont ajoutés automatiquement dans les modèles via
le code de `open_democracy_back.apps.ready`)
- envoyer en (pré-)prod le nouveau code
- ajouter la langue dans les paramètres de wagtail
- redémarrer le service web (via supervisor) pour que les changements soient bien pris
en compte

### Ajouter des champs à traduire

- sur le modèle concerné, iniqué la liste des `translated_fields`
- lancer `makemigrations`
- modifier le fichier de migration, cf migraion 0056 pour
  - définir la fonction `fill_fr_fields`
  - définir les nouveaux champs à remplir par cette fonction
  - ajouter à la fin la migration `migrations.RunPython(fill_models_fr_fields, migrations.RunPython.noop),`

### Mettre à jour la base de donnée

    python manage.py makemigrations
    python manage.py migrate

### Mettre à jour l'index pour la fonction de recherche

To update the index and make work de search function :

```bash
python manage.py update_index
```


### Mettre à jour les traductions :

- Créer ou mettre à jour un fichier de traductions :
    `django-admin makemessages -l fr`
- Renseigner à la main les traductions dans les fichiers .po autogénéré
- Compiler les fichiers de traductions:
    `django-admin compilemessages`

### Utilisation de l'app django Tweets

Cf le README correspondant à l'app Tweets


### Système de traduction utilisé

Le système de traduction utilisé est [wagtail-localize](https://www.wagtail-localize.org/)
> Attention : Si une langue est rajouté il faudra (en plus du système de base de wagtail localize) adapter le switch de langue du header



### Commit de suppression des questions avec classement

https://gitlab.com/telescoop/democratie-ouverte/back/-/commit/7a901bffae7f54ead328b4d84819fa2716b1786b
