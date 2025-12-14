# Usage d’IA générative (section à inclure dans le rapport)

## Comment l’IA a été utilisée

- Aide à la structuration du rapport (plan, reformulation, synthèses).
- Aide au débogage (scripts `compresser`/`decompresser`, formats I/O, tests).
- Aide à l’interprétation des résultats expérimentaux.

## Analyse critique

Points positifs :
- accélère la rédaction et la clarification des concepts (NYT, symétrie, format de flux),
- aide à détecter rapidement des incohérences (ex. arrêt de décompression, format des logs).

Risques / limites :
- possibles confusions “caractère Unicode” vs “octet UTF‑8” si l’on ne vérifie pas sur le code,
- suggestions d’optimisation à valider expérimentalement,
- nécessité de relire et tester systématiquement (round-trip).

## Estimation quantitative (à compléter)

- proportion de code généré / modifié avec assistance IA : XX\%.
- proportion de texte du rapport influencé par IA : XX\%.

## Traçabilité (recommandé)

Indiquer brièvement :
- quelles parties ont été générées,
- quelles parties ont été vérifiées / adaptées,
- quels tests ont été utilisés pour valider les modifications.
