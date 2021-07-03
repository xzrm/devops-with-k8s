import os

from flask import (
    Flask,
    request,
    jsonify,
    abort,
    Response,
    g
)
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import json
import asyncio
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed
from typing import Dict
import signal

app = Flask(__name__)
db = SQLAlchemy(app)
app.config.from_object("project.config.Config")

CORS(app)


class Todo(db.Model):
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(140), unique=False)
    is_completed = db.Column(db.Boolean)

    def __init__(self, task):
        self.task = task
        self.is_completed = False

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return '<Todo {}, is done? {}>'.format(self.task, self.is_completed)


@app.teardown_appcontext
def shutdown_session(error):
    db.session.remove()
    if error:
        print(error)


@app.route('/todo')
def get_todos():
    todos = db.session.query(Todo).all()
    return jsonify([i.as_dict() for i in todos])


@app.route('/todo', methods=['POST'])
async def create_todo():
    if request.method == 'POST':
        if not request.json or not 'task' in request.json:
            abort(400)
        todo = Todo(request.json['task'])
        db.session.add(todo)
        db.session.commit()
        await send_status_message({"type": "ADD", **todo.as_dict()})
        return jsonify(todo.as_dict()), 201


@app.route('/todo/<int:id>', methods=['GET', 'PUT', 'DELETE'])
async def get_or_update_todo(id):
    todo = Todo.query.get_or_404(id)

    if request.method == 'PUT':
        todo.is_completed = not todo.is_completed
        db.session.commit()
        await send_status_message({"type": "UPDATE", **todo.as_dict()})
        return jsonify(todo.as_dict()), 201

    elif request.method == 'DELETE':
        db.session.delete(todo)
        db.session.commit()
        await send_status_message({"type": "DELETE", **todo.as_dict()})
        return Response(status=201)

    return jsonify(todo.as_dict()), 201


async def send_status_message(msg: Dict):
    nc = NATS()
    loop = asyncio.get_event_loop() 
    try:
        await nc.connect(servers=app.config['NATS_URI'],
                        loop=loop,
                        connect_timeout=5)

    except Exception as e:
        print(e)
    
    try:
        print("sending status message")
        await nc.publish("updates", json.dumps(msg).encode())
    except ErrConnectionClosed:
        print("Connection closed prematurely")

    if nc.is_connected:
        await nc.flush()
        await nc.close()

    if nc.is_closed:
        print("Disconnected.") 
    
    return 1

