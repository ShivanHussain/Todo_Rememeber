import os
from flask import Flask, request, jsonify, render_template, redirect
from database import init_db
from models.task_model import create_task, get_all_tasks, get_task_by_id, update_task, delete_task

app = Flask(__name__)
init_db()  # optional index creation

# ---- API Routes ----
@app.route("/tasks", methods=["GET"])
def list_tasks():
    tasks = get_all_tasks()
    for t in tasks:
        t["_id"] = str(t["_id"])
    return jsonify(tasks)

@app.route("/tasks", methods=["POST"])
def add_task_api():
    data = request.json
    task_id = create_task(data)
    return jsonify({"task_id": task_id}), 201

@app.route("/tasks/<task_id>", methods=["GET"])
def get_task_api(task_id):
    task = get_task_by_id(task_id)
    if task:
        task["_id"] = str(task["_id"])
        return jsonify(task)
    return jsonify({"error": "Task not found"}), 404

@app.route("/tasks/<task_id>", methods=["PUT"])
def update_task_api(task_id):
    data = request.json
    updated = update_task(task_id, data)
    return jsonify({"updated": updated})

@app.route("/tasks/<task_id>", methods=["DELETE"])
def delete_task_api(task_id):
    deleted = delete_task(task_id)
    return jsonify({"deleted": deleted})

# ---- Frontend Routes ----
@app.route("/", methods=["GET"])
def index():
    tasks = get_all_tasks()
    active_tasks = [t for t in tasks if t.get("status") != "Complete"]
    completed_tasks = [t for t in tasks if t.get("status") == "Complete"]

    # Convert ObjectId to string
    for t in active_tasks + completed_tasks:
        t["_id"] = str(t["_id"])

    return render_template(
        "index.html",
        active_tasks=[(t["_id"], t.get("title"), t.get("description"), t.get("status", "Start")) for t in active_tasks],
        completed_tasks=[(t["_id"], t.get("title"), t.get("status", "Complete")) for t in completed_tasks]
    )

@app.route("/add", methods=["POST"])
def add_task_form():
    title = request.form.get("title")
    description = request.form.get("description", "")
    create_task({"title": title, "description": description, "status": "Start"})
    return redirect("/")

@app.route("/status/<task_id>")
def change_status(task_id):
    task = get_task_by_id(task_id)
    if task:
        status_order = ["Start", "Pending", "Complete"]
        current_status = task.get("status", "Start")
        next_status_index = (status_order.index(current_status) + 1) % len(status_order)
        update_task(task_id, {"status": status_order[next_status_index]})
    return redirect("/")

@app.route("/update-desc/<task_id>", methods=["POST"])
def update_desc(task_id):
    description = request.form.get("description", "")
    if description:
        update_task(task_id, {"description": description})
    return redirect("/")

@app.route("/delete/<task_id>")
def delete_task_form(task_id):
    delete_task(task_id)
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
