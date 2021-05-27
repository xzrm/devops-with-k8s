from flask import Flask
import os
from pathlib import Path
from flask_sqlalchemy import SQLAlchemy
from flask import abort
import sys
import logging

# path = os.path.join('/', 'usr', 'src' ,'app', 'files')
# if not os.path.exists(path):
#     os.makedirs(path)

# file_path = os.path.join(path, 'count.txt')

app = Flask(__name__)

db_user = os.environ.get('POSTGRES_USER')
db_psw = os.environ.get('POSTGRES_PASSWORD')
db_name = os.environ.get('POSTGRES_DB')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{}:{}@postgres-svc.default:5432/{}'.format(
    db_user, db_psw, db_name
)
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Counter(db.Model):
    __tablename__ = "counter"
    id = db.Column(db.Integer, primary_key=True)
    count_val = db.Column(db.Integer, unique=False)

    def __init__(self, count_val):
        self.count_val = count_val

    def __repr__(self):
        return '<Count %r>' % self.count_val

# def write_to_file(txt):
#     with open(file_path, "w+") as f:
#         f.write(txt)



db.create_all()
db.session.commit()

@app.route('/healthz')
def healthcheck():
    try:
        c = Counter.query.one()
        if c:
            return "OK"
    except Exception as e:
        abort(500)


@app.route('/')
def index():
    c = Counter.query.filter_by(id=1).first()
    if c is not None:
        c.count_val += 1
    else:
        c = Counter(0)

    db.session.add(c)
    db.session.commit()
    # write_to_file(str(c.count_val))
    return "ping / pong {}".format(c.count_val)


@app.route('/count')
def count():
    c = Counter.query.filter_by(id=1).first()
    if c is not None:
        counter = c.count_val
        return {
            "count": counter
        }
    return {
        "count": "NaN"
    }
    

if __name__ == '__main__':
    print("starting")
    # print(path)
    app.run(debug=True, host='0.0.0.0', use_reloader=False)