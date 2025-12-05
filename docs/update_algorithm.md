# Algorithme de Mise à Jour (style FGK/Vitter)

Objectif :
- Incrémenter les poids après chaque symbole
- Maintenir l’ordre GDBH via des échanges par blocs

TODO :
- Implémenter `modification(symbol)` et `traitement(node)` dans le module update
- Implémenter `finBloc(node)` (fin de bloc de poids égal)
- Implémenter `swap_nodes(a, b)` en respectant les contraintes d’ascendance
