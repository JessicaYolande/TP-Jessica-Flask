from flask import Flask, abort

app = Flask(__name__)

taches = [
    {
        "id":1,
        "titre": "Réviser les décorateurs",
        "priorite": "haute",
        "terminee": False
    },
    {
        "id":2,
        "titre":"Installer Flask",
        "priorite": "normal",
        "terminee": True
    },
    {
        "id":3,
        "titre":"Lire la doc Jinja2",
        "priorite":"basse",
        "terminee": False
    }
]

@app.route("/")
def index():
    return "<h1>Mes taches</h1>"

@app.route("/taches/<int:id>")
def tache(id):
    print(type(id), id)

    for t in taches:
        if t["id"] == id:
            return t["titre"]

    
    abort(404)