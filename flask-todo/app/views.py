from flask import Blueprint, render_template, request, redirect
from app.models.todo import Todo
from app.utils.db import db

todo = Blueprint('todo', __name__)

@todo.route('/')
def index():
    tasks = Todo.query.all()
    return render_template('index.html', tasks=tasks)

@todo.route('/new', methods=['POST'])
def new_task():
    new_task = Todo(request.form['task_name'])
    db.session.add(new_task)
    db.session.commit()
    return redirect('/')

@todo.route('/update/<id>')
def update_task(id):
    task = Todo.query.get(id)
    task.status = not task.status
    db.session.commit()
    return redirect('/')

@todo.route('/delete/<id>')
def delete_task(id):
    task = Todo.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return redirect('/')