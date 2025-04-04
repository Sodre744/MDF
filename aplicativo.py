from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

DB_FILE = "participants.json"

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/")
def home():
    return "Bot MDF rodando com sucesso!"

@app.route("/votar", methods=["GET", "POST"])
def votar():
    if request.method == "POST":
        nome = request.form.get("nome")
        instagram = request.form.get("instagram")
        convidado = request.form.get("convidado")
        categoria = request.form.get("categoria")
        if not nome or not instagram or not categoria:
            return "Campos obrigatórios não preenchidos.", 400
        data = load_data()
        data.append({
            "nome": nome,
            "instagram": instagram,
            "convidado": convidado,
            "categoria": categoria
        })
        save_data(data)
        return redirect("/votar")
    return render_template("votar.html")

@app.route("/painel")
def painel():
    data = load_data()
    return render_template("painel.html", participantes=data)

@app.route("/vencedor")
def vencedor():
    data = load_data()
    if not data:
        return "Nenhum participante encontrado.", 404
    import random
    vencedor = random.choice(data)
    return render_template("vencedor.html", vencedor=vencedor)
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
