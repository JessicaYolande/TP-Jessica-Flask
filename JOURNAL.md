# Journal de découverte — Soa Rakoto

## Mission 1 — Découvrir Flask et le mode debug

- **Essayé :** créer une application Flask dans `app.py`, afficher le titre « Mes tâches » et lancer le serveur avec `flask --app app run`, puis avec `flask --app app run --debug`.
- **Observé :** la page d'accueil affiche le titre « Mes tâches ». En mode debug, Flask fournit des informations détaillées lorsqu'une erreur survient et recharge automatiquement l'application après certaines modifications du code.
- **Doc :** documentation officielle Flask — Quickstart, *A Minimal Application* et *Debugging Application Errors*.
- **Expliqué :** `Flask(__name__)` crée l'application. Le décorateur `@app.route("/")` associe l'URL `/` à la fonction `index()`. Cette fonction renvoie du HTML au navigateur. Le mode debug facilite le développement, mais ne doit pas être activé en production, car il peut exposer des informations sensibles.

### Code utilisé

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>Mes tâches</h1>"
```

### Expérience sur les erreurs

Pour provoquer une erreur, on peut remplacer temporairement le retour de la fonction par :

```python
return "<h1>Mes tâches</h1>" + 1
```

Cette instruction provoque une erreur de type `TypeError`, car Python ne peut pas additionner directement une chaîne de caractères et un entier.

---

## Mission 2 — Jouer avec les URL

- **Essayé :** ouvrir `/taches/2` pour afficher le titre de la deuxième tâche, puis tester un identifiant inconnu et une URL comme `/taches/abc`.
- **Observé :** `/taches/2` affiche le titre de la tâche correspondante. Un identifiant inexistant renvoie une erreur 404. La route utilisant `<int:id>` n'accepte pas une valeur non entière comme `abc`.
- **Doc :** documentation officielle Flask — Quickstart, *Variable Rules* et *Errors*.
- **Expliqué :** le convertisseur `<int:id>` transforme la partie correspondante de l'URL en entier avant d'appeler la fonction. Sans ce convertisseur, la valeur récupérée serait une chaîne de caractères, par exemple `"2"`, ce qui pourrait empêcher une comparaison avec l'entier `2`. `abort(404)` renvoie le code HTTP 404, qui indique que la ressource demandée est introuvable. En revanche, `return "Tache introuvable"` renvoie normalement le code 200 si aucun autre code n'est précisé.

### Exemple de route

```python
from flask import abort

@app.route("/taches/<int:id>")
def tache(id):
    for t in taches:
        if t["id"] == id:
            return t["titre"]

    abort(404)
```

---

## Mission 3 — Afficher les tâches avec Jinja

- **Essayé :** remplacer l'affichage brut de la liste par un template HTML utilisant une boucle, des conditions et des filtres Jinja.
- **Observé :** chaque tâche peut être affichée séparément, numérotée et accompagnée de sa priorité. Les tâches terminées peuvent être barrées. Le nombre de tâches restantes peut être calculé.
- **Doc :** documentation officielle Flask — *Templates* ; documentation Jinja — *Template Designer Documentation*.
- **Expliqué :** `render_template("taches.html", taches=taches)` transmet la liste Python au template. `{{ ... }}` affiche une expression, tandis que `{% ... %}` permet d'écrire des instructions telles que les boucles et les conditions. `loop.index` numérote les éléments à partir de 1. La condition `{% if t.terminee %}` permet de distinguer les tâches terminées des tâches actives. Les filtres Jinja, comme `upper`, `length` et `sort(attribute="titre")`, permettent de transformer ou de trier les données affichées.

### Découvertes complémentaires

- `{{ taches }}` affiche la représentation brute de la liste.
- `{{ inconnue }}` affiche généralement une chaîne vide avec la configuration standard de Jinja.
- La balise HTML `<del>` permet de barrer le texte d'une tâche terminée.
- Jinja n'interprète pas automatiquement le Markdown : écrire `**Important**` dans un template ne suffit pas à mettre le texte en gras.
- L'échappement automatique de Jinja protège généralement les templates HTML contre l'interprétation directe de balises HTML contenues dans les données.
- `{{ taches|rejectattr("terminee")|list|length }}` permet de compter les tâches dont l'attribut `terminee` est faux, avec la structure de données utilisée dans le TP.

---

## Mission 4 — Un menu commun

- **Essayé :** créer un template de base et une feuille de style commune, puis faire hériter la page des tâches de ce template.
- **Observé :** la page conserve la même structure générale, le même menu et la même mise en forme. Le contenu spécifique est inséré dans le bloc prévu à cet effet.
- **Doc :** documentation officielle Flask — *Templates* et *Static Files* ; documentation Jinja — *Template Inheritance*.
- **Expliqué :** `{% extends "base.html" %}` permet à un template d'hériter d'un autre. Les blocs `titre` et `contenu` définissent les parties personnalisables. `{{ super() }}` permet de conserver le contenu du bloc parent tout en lui ajoutant du texte. Flask recherche les templates dans le dossier `templates/` et permet de servir les fichiers statiques depuis `static/`. `url_for()` construit les URL des routes et des ressources statiques.

### Réalisations

- Création de `templates/base.html` avec la structure HTML commune.
- Création des blocs `titre` et `contenu`.
- Utilisation de `{% extends "base.html" %}` dans `taches.html`.
- Utilisation de `{{ super() }}` pour compléter le titre parent.
- Création de `static/style.css`.
- Liaison du fichier CSS avec `url_for('static', filename='style.css')`.
- Vérification de la page d'accueil et du chargement du CSS.

---

## Mission 5 — Ajouter une tâche

- **Essayé :** créer un formulaire permettant de saisir le titre et la priorité d'une tâche, puis envoyer les données au serveur.
- **Observé :** le formulaire s'affiche avec une requête GET. Après validation, la requête POST transmet les données à Flask. Les champs invalides et les doublons sont refusés. Après un ajout réussi, l'utilisateur est redirigé vers la liste des tâches.
- **Doc :** documentation officielle Flask — Quickstart, *Accessing Request Data*, *Redirects and Errors* et *Message Flashing*.
- **Expliqué :** la méthode GET sert à demander l'affichage d'une ressource, tandis que POST permet d'envoyer les données du formulaire. `request.form` récupère les valeurs envoyées. `strip()` retire les espaces au début et à la fin du titre. `casefold()` permet de comparer les titres sans distinguer les majuscules et les minuscules. La validation doit être effectuée côté serveur, même si le formulaire HTML utilise `required`. Après l'ajout, `redirect(url_for("index"))` redirige l'utilisateur vers la liste et évite qu'un simple rafraîchissement renvoie le formulaire POST.

### Réalisations

- Création de `templates/ajouter.html`.
- Création de la route `/ajouter` acceptant GET et POST.
- Récupération du titre et de la priorité avec `request.form`.
- Vérification du titre obligatoire.
- Vérification de la validité de la priorité.
- Détection des doublons avec `casefold()`.
- Génération d'un identifiant pour la nouvelle tâche.
- Redirection vers la page d'accueil après un ajout réussi.
- Ajout du lien « Ajouter une tâche » au menu commun.

### Limite observée

Les tâches sont stockées dans une liste Python en mémoire. Elles disparaissent donc lorsque le processus du serveur redémarre. Une base de données serait nécessaire pour conserver les données durablement.

---

## Mission 6 — Filtrer les tâches et mémoriser le choix

- **Essayé :** ouvrir `/?filtre=actives` et `/?filtre=terminees`, puis utiliser les liens « Toutes », « Actives » et « Terminées ».
- **Observé :** la liste affichée change selon le filtre choisi. Le filtre est mémorisé dans la session Flask. Les liens étaient présents dans le template, mais leur texte était invisible sur le fond blanc de la page.
- **Doc :** documentation officielle Flask — Quickstart, *The Request Object* et *Sessions* ; documentation Jinja — *Template Inheritance*.
- **Expliqué :** `request.args.get("filtre")` récupère la valeur du paramètre `filtre` dans l'URL. Des conditions Python permettent de sélectionner les tâches correspondantes. `session["filtre"]` mémorise le dernier choix de l'utilisateur entre les requêtes. Le problème d'affichage venait de la règle CSS `nav a`, qui appliquait une couleur blanche à tous les liens de navigation. En séparant les sélecteurs `header nav a` et `.filtres a`, les liens du menu principal et ceux des filtres peuvent recevoir des styles différents.

### Réalisations

- Récupération du filtre avec `request.args.get("filtre")`.
- Mémorisation du filtre avec `session`.
- Mise en place de trois catégories :
  - `toutes` : toutes les tâches ;
  - `actives` : les tâches non terminées ;
  - `terminees` : les tâches terminées.
- Filtrage de la liste avec des conditions Python.
- Transmission des variables `taches`, `filtre` et `restantes` au template `taches.html`.
- Ajout de trois liens de filtrage utilisant `url_for()`.
- Correction du CSS pour rendre les liens visibles.
- Vérification des filtres dans le navigateur.

### Ce que j'ai appris

- Lire un paramètre transmis dans l'URL.
- Filtrer une liste Python selon une condition.
- Utiliser les sessions Flask pour mémoriser une préférence.
- Transmettre des données de Flask à un template Jinja.
- Utiliser des classes CSS pour personnaliser certains éléments HTML.
- Diagnostiquer et corriger un problème d'affichage.

---

## Bilan personnel

Ce TP m'a permis de découvrir progressivement le fonctionnement d'une application web avec Flask. J'ai appris à créer des routes, à utiliser des paramètres d'URL, à gérer les erreurs 404, à afficher des données avec Jinja, à réutiliser une structure HTML grâce à l'héritage des templates et à mettre en forme les pages avec CSS.

J'ai également appris à créer un formulaire, à vérifier les données côté serveur, à empêcher les doublons et à rediriger l'utilisateur après un ajout. Enfin, j'ai découvert les paramètres d'URL et les sessions pour filtrer les tâches et mémoriser le choix de l'utilisateur.

Les difficultés rencontrées, notamment l'erreur 404 et les liens invisibles à cause du CSS, m'ont appris à tester le comportement de l'application et à rechercher l'origine d'un problème avant de modifier le code.

Une limite importante reste le stockage des tâches en mémoire : elles ne sont pas conservées après le redémarrage du serveur. Une prochaine amélioration serait d'utiliser une base de données pour rendre l'application plus durable.
