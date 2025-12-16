# Retour d'expérience (RETEX)

## Ce que j'ai appris et bien réalisé
L'approche TDD ne m'était pas familière en pratique, compte tenu de l'envergure réduite de mes précédents projets. Cependant, partir des tests plutôt que de l'implémentation s'est révélé très structurant.

Le fait d'avoir un cahier des charges détaillé dès le départ m'a permis d'écrire mes tests de manière intuitive. Notamment pour l'API, où il m'a suffi de suivre les fichiers `.yml` pour identifier tous les scénarios à tester. Je pense avoir bien planifié mes tests unitaires et d'intégration (via le mock du `PointSetManager`). Lors de l'implémentation, ces tests m'ont véritablement guidé et m'ont permis de vérifier que mon code couvrait tous les edge cases. Pour l'API, les tests étaient primordiaux pour valider le fonctionnement en l'absence du service `PointSetManager`.

## Ce que je ferais autrement (Points d'amélioration)
Le point faible concerne les tests de performance. Bien qu'utiles pour mesurer l'exécution, ils passent systématiquement sans vérifier si le temps de traitement est acceptable.
Avec le recul, je définirais des critères d'acceptation précis dès le départ (ex: "un traitement doit prendre moins de 50ms pour X points") pour que ces tests puissent échouer en cas de régression. Je me suis aussi rendu compte trop tard que j'avais oublié d'implémenter certains tests de performance prévus initialement dans mon plan.

## Évaluation du plan initial
Je trouve mon plan initial assez bon. Je n'ai pas eu besoin de retoucher mes tests, ce qui m'a permis d'avancer sereinement dans l'implémentation.
Une stratégie payante a été de définir d'abord les classes (pour le typage et l'écriture des tests) avant toute logique métier. C'est d'ailleurs principalement sur la structure interne de ces classes que des ajustements ont eu lieu par rapport à ma vision d'origine, alors que les tests, qui se contentaient d'appeler les méthodes publiques, sont restés stables.
