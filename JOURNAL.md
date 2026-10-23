## Mission 2 — Jouer avec les URL

### Objectif
Afficher une tâche à partir de son identifiant et signaler correctement les identifiants inconnus.

### Découverte 1 : que fait `<int:id>` ?

`<int:id>` demande à Flask de récupérer l’identifiant dans l’URL sous forme de nombre entier (`int`).

### Découverte 2 : pourquoi `/taches/abc` renvoie-t-il une erreur 404 ?

La route utilise `<int:id>`, qui accepte uniquement les valeurs pouvant être converties en nombres entiers. La valeur `abc` ne respecte donc pas cette règle, et Flask renvoie une erreur `404 Not Found`.

### Découverte 3 : quelle différence existe entre `return "Tache introuvable"` et `abort(404)` ?

- `return "Tache introuvable"` : Flask renvoie normalement le code HTTP `200 OK`, car la fonction retourne simplement du texte.
- `abort(404)` : Flask renvoie le code HTTP `404 Not Found`, qui indique correctement que la ressource demandée n’existe pas.

### Documentation officielle
[Documentation Flask — Quickstart : Variable Rules et Errors](https://flask.palletsprojects.com/en/stable/quickstart/)