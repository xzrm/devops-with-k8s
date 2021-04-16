from flask import Flask, render_template, request, redirect, url_for
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db_user = os.environ.get('POSTGRES_USER')
db_psw = os.environ.get('POSTGRES_PASSWORD')
db_name = os.environ.get('POSTGRES_DB')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{}:{}@postgres-svc.default:5432/{}'.format(
    db_user, db_psw, db_name
)
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Todo(db.Model):
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(140), unique=False)

    def __init__(self, todo):
        self.todo = todo

    def __repr__(self):
        return '<Todo %r>' % self.todo

db.create_all()
db.session.commit()

@app.route('/')
def index():
    todos = db.session.query(Todo).all()
    todos = [i.todo for i in todos]
    return render_template('index.html', todos=todos)

@app.route('/todo', methods=['POST'])
def submit_form():
    new_todo = request.form['todo-text']
    todo = Todo(new_todo)
    db.session.add(todo)
    db.session.commit()
    # todos.append(new_todo)
    return redirect(url_for('index'))

@app.route('/todo')
def get_todos():
    todos = db.session.query(Todo).all()
    todos = [i.todo for i in todos]
    return {"todos": todos}

@app.route('/del')
def delete_todos():
    num_del_todos = db.session.query(Todo).delete()
    db.session.commit()
    return {"num_del_todos": num_del_todos}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')