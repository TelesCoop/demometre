# Démomètre - code frontend

## Notes pour les développeurs

### Mettre à jour les traductions

#### Lorsqu'il y a des ajouts dans le code

1. lancer `yarn do-vue-i18n-extract` pour repérer où les traductions sont utilisées
   et d'éventuelles nouvelles chaînes à traduire
2. lancer `python3 translations.py` pour
    - mettre à jour les fichiers app.po avec les nouvelles chaines à traduire
    - mettre à jour les fichiers [locale].json avec les traductions du fichier app.po
3. commit et push
4. sur le site de traduction (POEditor), importer les fichiers app.po avec l'intégration Github

#### Lorsqu'il y a des mise à jour dans le site de traduction (POEditor)

1. exporter les traductions depuis POEditor
2. lancer `python3 translations.py`
3. commit et push

### Ordre d'une évaluation

Cf `userStep.ts` :

1. localisation pour trouver s'il existe déjà une évalution pour cette
   localité (commune ou EPCI) -> appelle `assessments/by-locality/`
   pour avoir la réponse. Si une évalution (autre que diagnostic rapide)
   a déja été créée pour cette localité, on rejoint cette évalution. Sinon,
   une nouvelle évaluation est créée.
2. si c'est une nouvelle évaluation, (sinon, on passe à l'étape suivante),
   sur `/evaluation/initialisation`
    - on choisit le type d'évaluation
    - on confirme qu'on accepte les conditions
    - on choisit le nom à afficher publiquement comme porteur et
      au nom de qui on évalue (asso / mairie)
3. sur `/evaluation/initialisation/[id]/question-objectives` on répond aux questions objectives
4. sur `/evaluation/initialisation/[id]/validation`, on valide les réponses aux questions objectives
