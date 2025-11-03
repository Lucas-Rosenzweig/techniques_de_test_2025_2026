# Plan de test – Triangulation

Le but de projet est d'implémenter le composant de triangulation et de le tester de manière rigoureuse.  
Donc le plan de test suivant est proposé pour couvrir les différents aspects du composant **triangulators** uniquement.

---

## Sommaire
1. [Tests unitaires](#1-tests-unitaires)  
   1.1 [Tests API](#tests-api)  
   1.2 [Tests fonctionnels](#tests-fonctionnels)  
2. [Tests d'intégration](#2-tests-dintégration)  
3. [Tests de performance](#3-tests-de-performance)  
4. [Qualité du code & couverture des tests](#4-qualité-du-code--couverture-des-tests)

---

## 1. Tests unitaires

Les tests unitaires sur le composant triangulators vont être réalisés en mockant le `PointSetManager`,  
qui est le principal fournisseur de données pour le module de triangulation.

### Tests API

On va vérifier que l'API répond correctement aux différents scénarios d'appel :

- **Test API 200** : Si on envoie un `PointSetId` valide, que la communication avec le `PointSetManager` est réussie, et que l'algorithme de triangulation ne renvoie pas d'erreur, alors on doit recevoir des triangles au bon format.
- **Test API 400** : Si on envoie un `PointSetId` invalide (ex: format incorrect), on doit recevoir une erreur 400.
- **Test API 404** : Si on envoie un `PointSetId` valide mais que le `PointSetManager` ne trouve pas le `PointSet` correspondant, on doit recevoir une erreur 404.
- **Test API 500** : Si la communication avec le `PointSetManager` échoue (ex: timeout, erreur réseau), on doit recevoir une erreur 500.
- **Test API 503** : Si l'algorithme de triangulation rencontre une erreur interne (ex: exception non gérée), on doit recevoir une erreur 503.

Pour les tests API ci-dessus, le mock du `PointSetManager` devra simuler les différents scénarios.  
Ces tests permettent de vérifier la partie *interface* du composant triangulators : on est sûr que les appels API sont correctement gérés selon les différents cas.

> Exemple :  
> Dans le premier test, le mock va retourner un `PointSet` valide pour un `PointSetId` donné.  
> Dans le test 404, il simule l’absence de `PointSet`.  
> Dans le test 500, il simule une erreur de communication.  
> Le fichier `point_set_manager.yml` permettra de mocker ces différents scénarios.

### Tests fonctionnels

Tests spécifiques à l'implémentation de l'algorithme de triangulation sans passer par l'API.  
Ces tests sont basés sur les cas remarquables suivants :

- Test de sérialisation/désérialisation : Vérifier que la conversion entre le format binaire et le format interne fonctionne correctement.
- Test avec un `PointSet` vide → 0 triangles (ou erreur selon l'implémentation).
- Test avec des points dupliqués → 0 triangles (ou erreur selon l'implémentation).
- Test avec 1 point → 0 triangles (ou erreur selon l'implémentation)..
- Test avec 2 points → 0 triangles (ou erreur selon l'implémentation)..
- Test avec des points alignés → 0 triangles (ou erreur selon l'implémentation)..
- Test avec 3 points → 1 triangle.
- Test avec 4 points formant un carré → 2 triangles.
- Test avec un `PointSet` quelconque dont le résultat attendu est connu.
- Test de validité du format des triangles générés , doit respecter le format spécifié.
Ces tests vérifient le bon fonctionnement de l'algorithme dans des cas particuliers et couvrent les edge cases.

---

## 2. Tests d'intégration

L’implémentation de tests d’intégration pour le composant triangulators est limitée par l’absence d’autres composants réels avec lesquels il pourrait s’intégrer.  
Il n’y a donc **pas de tests d’intégration possibles** dans le cadre de ce projet.

Cependant, en condition réelle, des tests d'intégration seraient réalisés avec les composants suivants :

- **PointSetManager** : vérifier la récupération des `PointSet`.
- **Système de stockage des résultats** : vérifier que les triangles générés sont bien stockés et accessibles.
- **Interface utilisateur** : vérifier que les utilisateurs peuvent demander une triangulation et recevoir les résultats.

⚠️ On peut tout de même réaliser des tests d'intégration limités à l'aide de *mocks* :

- **Test d'intégration avec un mock du PointSetManager** : vérifier que le composant triangulators peut récupérer un `PointSet` simulé et effectuer la triangulation.

Ce test permet de valider le workflow complet : récupération des données + traitement.

---

## 3. Tests de performance

Les tests de performance pour le composant triangulators se concentreront sur :

- le temps de traitement
- l’utilisation des ressources (CPU, mémoire)

Paramètres testés :

- Taille du `PointSet` : 10², 10³, 10⁴, 10⁵, 10⁶
- Amplitude des coordonnées :  
  Ex : 0–100, 0–10 000, −1000 à 1000
- Distribution des points :  
  Répartition uniforme, clusters, alignement linéaire

Tests associés :

- Temps de conversion (format interne ↔ format binaire)
- Temps de triangulation

Chaque test mesurera temps + ressources consommées.

Des test de performances peuvent aussi être réalisés sur l'api en mesurant le temps de réponse pour différentes tailles de `PointSet`.

---

## 4. Qualité du code & couverture des tests

- Qualité du code assurée par **ruff** (config dans `pyproject.toml`)
- Couverture mesurée par **coverage**  
  🎯 Objectif : **100%**

Possibilité d’ajouter :

- **GitHub Actions** pour refuser un commit non conforme
- Génération automatique de la documentation avec `pdoc3` à chaque commit sur `main`

