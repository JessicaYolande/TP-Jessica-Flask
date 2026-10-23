
from flask import (
    Flask, abort, render_template, request,
    redirect, url_for, flash, session
)

app = Flask(__name__)

# Remplacer par la clé générée dans le terminal
app.secret_key = "6ad3f8435bab38a623547607950a86717dc589056ca77cbe17e9671363e01ad7"

taches = [
    {
        "id": 1,
        "titre": "Réviser les décorateurs",
        "priorite": "haute",
        "terminee": False
    },
    {
        "id": 2,
        "titre": "Installer Flask",
        "priorite": "normal",
        "terminee": True
    },
    {
        "id": 3,
        "titre": "Lire la doc Jinja2",
        "priorite": "basse",
        "terminee": False
    }
]


@app.route("/")
def index():
    filtre = request.args.get("filtre")

    if filtre is None:
        filtre = session.get("filtre", "toutes")

    if filtre not in ["toutes", "actives", "terminees"]:
        filtre = "toutes"

    session["filtre"] = filtre

    if filtre == "actives":
        taches_affichees = [t for t in taches if not t["terminee"]]
    elif filtre == "terminees":
        taches_affichees = [t for t in taches if t["terminee"]]
    else:
        taches_affichees = taches

    restantes = sum(1 for t in taches if not t["terminee"])

    return render_template(
        "taches.html",
        taches=taches_affichees,
        restantes=restantes,
        filtre=filtre
    )


@app.route("/taches/<int:id>")
def tache(id):
    for t in taches:
        if t["id"] == id:
            return t["titre"]

    abort(404)


@app.route("/ajouter", methods=["GET", "POST"])
def ajouter():
    if request.method == "POST":
        titre = request.form.get("titre", "").strip()
        priorite = request.form.get("priorite", "")

        if not titre:
            return "Erreur : le titre est obligatoire.", 400

        if priorite not in ["basse", "normal", "haute"]:
            return "Erreur : priorité invalide.", 400

        for t in taches:
            if t["titre"].casefold() == titre.casefold():
                return "Erreur : cette tâche existe déjà.", 400

        nouvel_id = max((t["id"] for t in taches), default=0) + 1

        taches.append({
            "id": nouvel_id,
            "titre": titre,
            "priorite": priorite,
            "terminee": False
        })

        flash("Tâche ajoutée")
        return redirect(url_for("index"))

    return render_template("ajouter.html")
