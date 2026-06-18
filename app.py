import os

from flask import Flask, request, jsonify, render_template, redirect

from database import init_db
from models.task_model import (
    create_task,
    get_all_tasks,
    get_task_by_id,
    update_task,
    delete_task,
)

app = Flask(__name__)
init_db()  # optional index creation


# ---- API Routes ----
@app.route("/tasks", methods=["GET"])
def list_tasks():
    tasks = get_all_tasks()
    for task in tasks:
        task["_id"] = str(task["_id"])
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

    active_tasks = [
        task for task in tasks
        if task.get("status") != "Complete"
    ]

    completed_tasks = [
        task for task in tasks
        if task.get("status") == "Complete"
    ]

    # Convert ObjectId to string
    for task in active_tasks + completed_tasks:
        task["_id"] = str(task["_id"])

    active_task_data = [
        (
            task["_id"],
            task.get("title"),
            task.get("description"),
            task.get("status", "Start"),
        )
        for task in active_tasks
    ]

    completed_task_data = [
        (
            task["_id"],
            task.get("title"),
            task.get("status", "Complete"),
        )
        for task in completed_tasks
    ]

    return render_template(
        "index.html",
        active_tasks=active_task_data,
        completed_tasks=completed_task_data,
    )


@app.route("/add", methods=["POST"])
def add_task_form():
    title = request.form.get("title")
    description = request.form.get("description", "")

    create_task(
        {
            "title": title,
            "description": description,
            "status": "Start",
        }
    )

    return redirect("/")


@app.route("/status/<task_id>")
def change_status(task_id):
    task = get_task_by_id(task_id)

    if task:
        status_order = ["Start", "Pending", "Complete"]
        current_status = task.get("status", "Start")

        next_status_index = (
            status_order.index(current_status) + 1
        ) % len(status_order)

        update_task(
            task_id,
            {"status": status_order[next_status_index]},
        )

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
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
    )
