from datetime import datetime, timedelta
import json
import os

from flask import Flask, redirect, render_template, request


app = Flask(__name__)
FILE_NAME = "entries.json"


def load_tasks():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
    return []


def save_tasks(tasks):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


tasks = load_tasks()


@app.route("/")
def index():
    return render_template("index.html", tasks=tasks)


@app.route("/add")
def add_get():
    return render_template("add.html")


@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()
    if content:
        tasks.append(
            {
                "title": title,
                "content": content,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            }
        )
        save_tasks(tasks)
    return redirect("/")


@app.route("/detail/<int:task_id>", methods=["GET"])
def detail_task(task_id):
    return render_template("detail.html", task=tasks[task_id])


@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        save_tasks(tasks)
    return redirect("/")


@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    if task_id < 0 or task_id >= len(tasks):
        return "Задача не найдена", 404

    if len(tasks[task_id]["content"]) == 0:
        return redirect("/") 

    if request.method == 'POST':
        new_title = request.form.get("title", '').strip()
        new_content = request.form.get('content', '').strip()

        if new_content:
            tasks[task_id]['content'] = new_content
            save_tasks(tasks)
        if new_title:
            tasks[task_id]['title'] = new_title
            save_tasks(tasks)
        return redirect('/')

    else:
        return render_template('edit.html', task=tasks[task_id])

if __name__ == "__main__":
    app.run(debug=True)