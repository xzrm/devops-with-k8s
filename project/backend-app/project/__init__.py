from flask import (
    Flask,
    request,
    jsonify,
    abort,
    Response,
)
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import json
from pynats import NATSClient


app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)
# print(app.config)
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


@app.route('/todo')
def get_todos():
    todos = db.session.query(Todo).all()
    return jsonify([i.as_dict() for i in todos])


@app.route('/todo', methods=['POST'])
def create_todo():
    if request.method == 'POST':
        if not request.json or not 'task' in request.json:
            abort(400)
        todo = Todo(request.json['task'])
        db.session.add(todo)
        db.session.commit()
        send_status_message({"type": "ADD", **todo.as_dict()})
        return jsonify(todo.as_dict()), 201


@app.route('/todo/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def get_or_update_todo(id):
    todo = Todo.query.get_or_404(id)

    if request.method == 'PUT':
        todo.is_completed = not todo.is_completed
        db.session.commit()
        send_status_message({"type": "UPDATE", **todo.as_dict()})
        return jsonify(todo.as_dict()), 201

    elif request.method == 'DELETE':
        db.session.delete(todo)
        db.session.commit()
        send_status_message({"type": "DELETE", **todo.as_dict()})
        return Response(status=201)

    return jsonify(todo.as_dict()), 201


def send_status_message(msg):
    try:
        with NATSClient(app.config["NATS_URI"], socket_timeout=2) as client:
            client.publish("updates", payload=json.dumps(msg).encode())
    except Exception as e:
        print(e)


# def send_status_message(msg: Dict):
#     print("Connecting to ", app.config["RABBITMQ_URI"])
#     connection = pika.BlockingConnection(pika.ConnectionParameters(host=app.config["RABBITMQ_URI"]))
#     channel = connection.channel()
#     channel.queue_declare(queue="updates", durable=True) #if Rabbitmq dies, the task is not lost
#     channel.basic_publish(
#         exchange="",
#         routing_key="updates",
#         body=json.dumps(msg).encode(),
#         properties=pika.BasicProperties(
#             delivery_mode=2,  
#         ))

#     connection.close()
