from flask import Flask
import os
from pathlib import Path


counter = 0
path = os.path.join('/', 'usr', 'src' ,'app', 'files')
if not os.path.exists(path):
    os.makedirs(path)

file_path = os.path.join(path, 'count.txt')

app = Flask(__name__)

def write_to_file(txt):
    with open(file_path, "w+") as f:
        f.write(txt)


@app.route('/')
def index():
    global counter
    tmp = counter
    counter += 1
    write_to_file(str(tmp))
    return "pong {}".format(tmp)


@app.route('/count')
def count():
    return {
        "count": counter
    }




if __name__ == '__main__':
    print("starting")
    print(path)
    app.run(debug=True, host='0.0.0.0')