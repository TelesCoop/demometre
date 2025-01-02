# Tests d'intégration (end-to-end)

## Checklist

- [x] Parcours du questionnaire
  - [x] Évaluation rapide
  - [x] Évaluation participative
  - [x] Évaluation avec expert
- [x] Questions conditionnelles
  - [x] En fonction du profilage
  - [x] En fonction du rôle
- [x] Tableau de bord
  - [x] Critère de représentativité
- [x] Résultats
  - [x] publiés pour une évaluation rapide
  - [x] publiés pour une évaluation participative uniquement lorsque le critère de représentativité est atteint
  - [x] les résultats sont corrects, y compris les graphiques pour les 4 représentations

## Description des tests

### Le questionnaire

#### Les données

Le questionnaire comporte 13 questions :
- la question sur le rôle
- 2 questions de profilage
- 6 questions subjectives, 1 de chaque type (choix unique, choix multiple, oui/non, fermée à échelle, pourcentage, nombre)
dans le pilier Représentation
- 3 questions conditionnelles (deux en fonction du profilage, une en fonction du rôle) dans le pilier Transparence
- 1 question objective dans le pilier Participation

Le tableau de bord n'a qu'un critère de représentativité, correspondant à la première question de profilage,
avec 3 réponses possibles et une valeur de 25% minimum pour chaque question.

#### Évaluation rapide

- parcours du questionnaire dans un cas simple (aucune question conditionnelle)
  - vérification que les résultats sont disponibles
- parcours du questionnaire dans avec les deux questions conditionnelles de profilage
- parcours du questionnaire dans avec la question de profilage

#### Évaluation participative

- parcours du questionnaire dans un cas simple (aucune question conditionnelle)
- parcours du questionnaire dans avec les deux questions conditionnelles de profilage
  - vérification que les résultats ne sont pas encore disponible
    (personne n'a répondu la 3e réponse de la première question de profilage)
- parcours du questionnaire dans avec la question de profilage
  - vérification que les résultats sont disponibles
    (le critère de représentativité est maintenant atteint)

#### Évaluation avec expert

- parcours du questionnaire dans un cas simple (aucune question conditionnelle)

### Autre

Le parcours connexion et consultation du compte
