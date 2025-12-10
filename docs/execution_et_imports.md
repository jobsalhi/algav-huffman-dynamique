# Exécution des modules, `-m` et `__main__`

Ce projet est organisé comme un paquet Python (`encoder`, `decoder`, `core`, `tests`, etc.). Pour bien utiliser les scripts et les tests, il est important de comprendre deux mécanismes :

- l’option `-m` de Python ;
- la condition `if __name__ == "__main__":` dans les fichiers.

## Exécuter un module avec `python -m`

Quand on lance :

```bash
python -m tests.test_roundtrip_basic
```

Python cherche le module `tests.test_roundtrip_basic` **dans le paquet courant**, puis l’exécute. Avantages :

- les imports relatifs au projet fonctionnent, par exemple :
  ```python
  from encoder.compressor import encode_file
  ```
  car `encoder` est vu comme un sous-paquet du projet ;
- on évite les erreurs du type `ModuleNotFoundError: No module named 'encoder'` qui arrivent souvent quand on fait directement :
  ```bash
  python tests/test_roundtrip_basic.py
  ```

Pour ce projet, les commandes recommandées sont :

```bash
# depuis la racine du repo
python -m encoder.compressor input.txt output.huff
python -m decoder.decompressor input.huff output.txt
python -m tests.test_roundtrip_basic
```

## Rôle de `if __name__ == "__main__":`

Dans chaque fichier Python, la variable spéciale `__name__` dépend de la façon dont le fichier est utilisé :

- si le fichier est **exécuté** (script ou `-m`), alors `__name__ == "__main__"` ;
- s’il est **importé** comme module, alors `__name__` vaut le nom du module (par exemple `"encoder.compressor"`).

On utilise donc :

```python
if __name__ == "__main__":
    # code exécuté seulement quand on lance directement le module
    ...
```

Cela permet de séparer :

- la **partie bibliothèque** (fonctions/classes réutilisables) ;
- la **partie interface en ligne de commande** (lecture d’arguments, `print`, petits tests manuels).

### Application dans ce projet

- Dans `encoder/compressor.py` :
  - la fonction `encode_file(input_path, output_path)` est la partie "bibliothèque" ;
  - le bloc `if __name__ == "__main__":` lit les arguments de la ligne de commande et appelle `encode_file` quand on lance :
    ```bash
    python -m encoder.compressor fichier.txt fichier.huff
    ```

- Dans `decoder/decompressor.py` :
  - la fonction `decode_file(input_path, output_path)` est la partie "bibliothèque" ;
  - le bloc `if __name__ == "__main__":` permet d’écrire :
    ```bash
    python -m decoder.decompressor fichier.huff fichier.txt
    ```

- Dans `tests/test_roundtrip_basic.py` :
  - le cœur du fichier définit `roundtrip(input_path)` qui utilise
    `encode_file` et `decode_file` ;
  - le bloc `if __name__ == "__main__":` sert uniquement à lancer quelques tests simples quand on exécute :
    ```bash
    python -m tests.test_roundtrip_basic
    ```

Ainsi, les mêmes fichiers peuvent :

- être importés tranquillement dans d’autres modules (`from encoder.compressor import encode_file`) ;
- ou être exécutés comme petits programmes de test/CLI grâce à `python -m ...` et au bloc `__main__`.
