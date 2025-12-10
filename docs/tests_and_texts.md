# Jeux de tests et observations

Ce document résume les fichiers de test présents dans `io/input` et les types
d'observations que l'on peut faire avec l'encodeur/décodeur Huffman dynamique.

## 1. Fichiers dans `io/input`

- `short.txt`  
  Petit texte très court (par ex. `éA`). Sert surtout à vérifier que :
  - la compression/décompression fonctionne sur de très petits fichiers ;
  - l'UTF-8 est bien géré (caractère accentué + ASCII).

- `random_uniform_letters.txt`  
  Lettres de `A` à `Z` avec une distribution approximativement uniforme.  
  **Observation attendue** :
  - peu de structure statistique → taux de compression proche de 1 (voire > 1
    à cause de l'en-tête et des métadonnées) ;
  - illustre le cas défavorable pour Huffman dynamique.

- `random_biased_letters.txt`  
  Texte biaisé : beaucoup de `A`, quelques `B`, très peu de `C` et `D`.  
  **Observation attendue** :
  - meilleur taux de compression que le cas uniforme, car l'algorithme
    exploite la forte fréquence de `A` ;
  - montre l'intérêt de Huffman dès qu'il y a une distribution non uniforme.

- `code_python_sample.txt`  
  Petit fichier de code Python (définition de fonctions, `if __name__ == ...`).  
  **Observation attendue** :
  - présence de nombreux symboles structurés (`(`, `)`, `:`, `=`, indentations) ;
  - compression généralement correcte, mais souvent un peu moins bonne que du
    texte en langue naturelle, car la redondance est différente.

- `data_json_sample.txt`  
  Données de type JSON (liste d'utilisateurs avec champs `id`, `name`, `roles`).  
  **Observation attendue** :
  - beaucoup de symboles répétés (`"id"`, `"name"`, accolades, crochets, virgules) ;
  - bon candidat pour une compression intéressante malgré l'absence de phrases.

- `gutenberg_small_fr.txt`  
  Court extrait de texte en français, inspiré de Gutenberg.  
  **Observation attendue** :
  - cas représentatif de texte naturel en français ;
  - normalement un des meilleurs taux de compression (mots fréquents,
    structure linguistique forte).

- `english_mixed_case.txt`  
  Petit texte en anglais avec majuscules/minuscules, chiffres et ponctuation.  
  **Observation attendue** :
  - permet de comparer les effets de la casse et des chiffres ;
  - taux de compression intermédiaire entre texte très structuré et aléatoire.

- `json_like_config.txt`  
  Fichier de configuration de style JSON (service, retries, endpoints...).  
  **Observation attendue** :
  - proche d'un fichier `.json` réel ;
  - intéressant pour la Question 10 (fichier structuré non linguistique).

## 2. Comment exploiter ces fichiers dans le rapport

1. **Pour la Question 8 (texte naturel)** :
   - utiliser `gutenberg_small_fr.txt` (et éventuellement un extrait plus long
     de `Blaise_Pascal.txt`) ;
   - mesurer : taille originale, taille compressée, ratio, temps.

2. **Pour la Question 9 (fichiers aléatoires)** :
   - comparer `random_uniform_letters.txt` et `random_biased_letters.txt` ;
   - expliquer que l'un simule une distribution uniforme et l'autre une
     distribution biaisée ;
   - commenter la différence de taux de compression.

3. **Pour la Question 10 (fichiers non naturels)** :
   - utiliser `code_python_sample.txt`, `data_json_sample.txt` et
     `json_like_config.txt` ;
   - expliquer qu'il s'agit d'information structurée (code, données) et non de
     texte en langue naturelle ;
   - discuter les résultats obtenus par rapport aux fichiers purement textuels.

4. **Pour la Question 11 (analyse globale)** :
   - rassembler les résultats de tous ces fichiers (par exemple via
     `tests/test_roundtrip_basic.py` et/ou les scripts `compresser` / `decompresser`) ;
   - construire un tableau ou une figure montrant : type de fichier → ratio de
     compression → temps ;
   - relier les observations à la théorie :
     - plus la distribution des symboles est déséquilibrée, meilleur est
       Huffman ;
     - les en-têtes et la structure dynamique coûtent relativement plus cher sur
       les très petits fichiers ;
     - le travail à l'octet (UTF-8) limite un peu la compression pour les
       caractères multi-octets.

  ## 3. Résultats observés (extrait de `compression_report.csv`)

  Les tests automatisés (`python -m tests.test_roundtrip_basic`) ont produit
  le fichier `compression_report.csv` avec les résultats suivants (ratio =
  taille_compressée / taille_originale) :

  - `short.txt` : 3 B → 12 B (**ratio ≈ 4.00**, sur‑coût lié à l'en-tête et à la
    structure dynamique sur un fichier minuscule).
  - `random_uniform_letters.txt` : 780 B → 597 B (**ratio ≈ 0.77**).
  - `random_biased_letters.txt` : 527 B → 229 B (**ratio ≈ 0.43**).
  - `gutenberg_small_fr.txt` : 294 B → 215 B (**ratio ≈ 0.73**).
  - `english_mixed_case.txt` : 204 B → 177 B (**ratio ≈ 0.87**).
  - `code_python_sample.txt` : 628 B → 430 B (**ratio ≈ 0.68**).
  - `data_json_sample.txt` : 439 B → 322 B (**ratio ≈ 0.73**).
  - `json_like_config.txt` : 177 B → 149 B (**ratio ≈ 0.84**).

  ### Commentaires rapides

  - Les fichiers **très petits** (`short.txt`) se compressent mal car le coût
    fixe (64 bits de taille + structure de l'arbre) domine.
  - Le fichier **aléatoire uniforme** (`random_uniform_letters.txt`) a un ratio
    assez proche de 1 (≈ 0.77), comme attendu pour une distribution presque
    plate.
  - Le fichier **aléatoire biaisé** (`random_biased_letters.txt`) est celui qui
    se compresse le mieux (≈ 0.43), confirmant que Huffman profite fortement
    d'une distribution très déséquilibrée.
  - Les textes **naturels** (`gutenberg_small_fr.txt`, `english_mixed_case.txt`)
    ont des ratios intermédiaires (≈ 0.73–0.87), meilleurs que l'uniforme mais
    moins extrêmes que le cas très biaisé.
  - Les fichiers **non naturels** mais structurés (`code_python_sample.txt`,
    `data_json_sample.txt`, `json_like_config.txt`) se situent globalement dans
    la même zone que le texte naturel, parfois un peu mieux (`code_python_sample.txt`),
    ce qui montre que la redondance de la syntaxe (mots‑clés répétés, guillemets,
    virgules, accolades) est aussi bien exploitée par Huffman dynamique.
