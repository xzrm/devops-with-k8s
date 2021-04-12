from flask import Flask

counter = 0

app = Flask(__name__)

@app.route('/')
def index():
    global counter
    tmp = counter
    counter += 1
    return "pong {}".format(tmp)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')