# Plan de test Triangulation

Le but de projet est d'implémenter le composant de triangulation et de le tester de manière rigoureuse.
Donc le plan de test suivant est proposé pour couvrir les différents aspects du composant triangulators unquement.

## 1. Tests unitaires 

Les tests unitaires sur le composant triangulators vont être réalisés en mockant le PointSetManager
qui est le principal fournisseur de données pour le module de triangulation.

Test coté api, on va vérifier que l'api répond correctement aux différents scénarios d'appel.:
- Test API 200 : Si on envoie un PointSetId valide, que la communication avec le PointSetManager est réussie, et que l'algorithme de triangulation ne renvoie pas d'erreur alors , on doit recevoir Triangles au bon format.
- Test API 400 : Si on envoie un PointSetId invalide (ex: format incorrect), on doit recevoir une erreur 400.
- Test API 404 : Si on envoie un PointSetId valide mais que le PointSetManager ne trouve pas le PointSet correspondant, on doit recevoir une erreur 404.
- Test API 500 : Si la communication avec le PointSetManager échoue (ex: timeout, erreur réseau), on doit recevoir une erreur 500.
- Test API 503 : Si l'algorithme de triangulation rencontre une erreur interne (de type : exception non gérée etc...), on doit recevoir une erreur 503.
Pour les tests api ci dessus , le mock du PointSetManager devra simuler les différents scénarios.
Ces tests permettent de vérifier la partie "interface" du composant triangulators on est sur que les appels api sont correctement gérés selon les différents cas.


Ex: dans le premier test, le mock vas retourner un PointSet valide pour un PointSetId donné.
A l'inverse dans le test 404, le mock vas simuler l'absence du PointSet correspondant.
Et dans le test 500, le mock vas simuler une erreur de communication.
Le point_set_manager.yml nous permet de mocker correctement ces différents scénarios.

- Tests "fonctionnel":  Test spécifique a l'implémentation de l'algorithme de triangulation sans passer par l'api.
  Ces tests sont basés sur les cas "remarquables" suivants :
  - Test de sérialisation/désérialisation : Vérifier que la conversion entre le format binaire et le format interne fonctionne correctement.
  - Test avec un PointSet vide doit renvoyer 0 triangles / ou une erreur selon l'implémentation
  - Test avec un PointSet contenant des points dupliqués : doit renvoyer 0 triangles / ou une erreur selon l'implémentation
  - Test avec un PointSet avec 1 point : doit renvoyer 0 triangles / ou une erreur selon l'implémentation
  - Test avec un PointSet avec 2 points : doit renvoyer 0 triangles / ou une erreur selon l'implémentation
  - Test avec un PointSet avec des points alignés : doit renvoyer 0 triangles / ou une erreur selon l'implémentation
  - Test avec un PointSet avec 3 points : Renvoie un seul triangle
  - Test avec un PointSet avec 4 points formant un carré : Renvoie 2 triangles
  - Test avec un PointSet quelconque ou nous connaissons le résultat attendu
  - Test de vérification de la validité des triangles générés : S'assurer que les triangles générés respectent les propriétés géométriques attendues (ex: pas de chevauchement, sommets valides, etc.)
Ces tests permettent de vérifier que l'algorithme de triangulation fonctionne correctement pour des cas particuliers et gère les edeges cases.


## 2. Tests d'intégration
L'implémentation de tests d'intégration pour le composant triangulators est limitée par l'absence d'autres composants réels avec lesquels intégrer.
Il n'y a donc pas de tests d'intégration possibles dans le cadre de ce projet.
Cependant , en condition réelle, des tests d'intégration seraient réalisés avec les composants suivants :
- PointSetManager : Vérifier que le composant triangulators peut récupérer correctement les PointSets
- Système de stockage des résultats : Vérifier que les triangles générés sont correctement stockés et récupérables.
- Interface utilisateur : Vérifier que les utilisateurs peuvent demander une triangulation et recevoir les résultats correctement.
Cependant nous pouvous réaliser des tests d'intégration limités en utilisant des mocks pour simuler les interactions avec ces composants.
- Test d'intégration avec un mock du PointSetManager : Vérifier que le composant triangulators peut récupérer un PointSet simulé et effectuer la triangulation correctement.
Cela permet un test du workflow complet de la triangulation en intégrant la récupération des données et le traitement.

## 3. Tests de performance
Les tests de performance pour le composant triangulators se concentreront sur les aspects suivants :
 - Temps de traitement
 - Utilisation des ressources

Les tests seront réalisés en variants les paramètres suivants :
    - Taille du PointSet : Tester avec des PointSets de différentes tailles (ex: 10², 10³, 10⁴, 10⁵, 10⁶)
    - Amplitude des coordonnées : Tester avec des PointSets dont les coordonnées des points varient dans différentes plages (ex: 0-100, 0-10,000, -1,000 à 1,000)
    - Distribution des points : Tester avec des PointSets ayant différentes distributions de points (ex: uniformément répartis, regroupés en clusters, alignés le long d'une ligne)

- Test sur la conversion depuis/vers le format interne/format binaire 
- Test sur la triangulation

Chaque test mesurera le temps de traitement et l'utilisation des ressources (CPU, mémoire) pour chaque combinaison de paramètres.

## 4. Qualité du code & couverture des tests
La qualitée du code est assurée par ruff dans le fichier pyproject.toml
La couverture est mesurée par coverage , avec un objectif de couverture de 100%

On peux envisager l'ajout de Github Actions pour par exemple refuser un commit qui ne respecte pas les règles de qualité.
Et un autre qui genère une documentation avec pdoc3 automatiquement à chaque commit sur la branche principale.


