from flask import Flask, render_template, request, redirect
from database import init_db, get_task_count, add_tasks, get_all_tasks, delete_tasks, get_tasks, update_task
from datetime import date

app = Flask(__name__)

# Инициализируем базу данных при запуске приложения
# Вызываем функцию init_db(), которая создаёт таблицу messages, если её ещё нет
# Это происходит один раз при старте сервера
init_db()


@app.route('/')
def index():
    tasks = get_all_tasks()
    total_count = get_task_count()
    return render_template(
        'index.html', tasks=tasks, total_count=total_count,
    )


@app.route('/detail/<int:item_id>', methods=['GET'])
def get_task(item_id):
    task = get_tasks(item_id)
    return render_template('detail.html', task=task)


@app.route('/add', methods=['POST'])
def add_task():
    title = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()
    if title and content:
        item = add_tasks(title, content, date.today().strftime('%Y-%m-%d'))
    return redirect("/")


@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_task(item_id):
    if request.method == 'POST':
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        update_task = update_task(title, content, date.today().strftime('%Y-%m-%d'), item_id)
        return redirect('/')
    return render_template('edit.html', task=item_id)


@app.route('/delete/<int:item_id>')
def delete_task(item_id):
    delete_tasks(item_id)
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)