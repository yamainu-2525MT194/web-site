
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

tasks = [
    {"id": 1, "title": "Learn Python", "done": False},
    {"id": 2, "title": "Learn React", "done": False},
]

@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)

@app.route("/api/tasks", methods=["POST"])
def add_task():
    data = request.json
    new_task = {"id": len(tasks)+1, "title": data["title"], "done": False}
    tasks.append(new_task)
    return jsonify(new_task), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
