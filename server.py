from flask import Flask, jsonify, request
import json
if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
 
app = Flask(__name__)
DB_FILE = 'todos.json'
 
# Hjelpefunksjon for å lese fra JSON-filen
def load_data():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, 'r') as f:
        return json.load(f)
 
# Hjelpefunksjon for å lagre til JSON-filen
def save_data(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)
 
# 1. Hente liste med alle notater (Kun ID og Tittel)
@app.route('/todos', methods=['GET'])
def get_all_todos():
    data = load_data()
    # Vi mapper gjennom lista for å bare returnere id og title per oppgave
    summary = [{"id": item["id"], "title": item["title"]} for item in data]
    return jsonify(summary)
 
# 2. Hente ett spesifikt notat basert på ID
@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    data = load_data()
    # Finn elementet som har riktig ID
    todo = next((item for item in data if item["id"] == todo_id), None)
    if todo:
        return jsonify(todo)
    return jsonify({"error": "Notat ikke funnet"}), 404
 
# 3. Opprette nytt notat
@app.route('/todos', methods=['POST'])
def create_todo():
    new_data = request.json
    data = load_data()
    # Generer ny ID (høyeste nåværende ID + 1)
    new_id = max([item["id"] for item in data], default=0) + 1
    new_entry = {
        "id": new_id,
        "title": new_data.get("title"),
        "tasks": new_data.get("tasks", [])
    }
    data.append(new_entry)
    save_data(data)
    return jsonify({"message": "Notat opprettet", "id": new_id}), 201

