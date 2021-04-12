from flask import Flask
import os
app = Flask(__name__)


USER = os.getenv('API_USER')
SECRET = os.getenv('SECRET')


@app.route('/')
def index():
    return "hello {user}".format(user=USER)

@app.route('/secret')
def secret():
    return "your secret {s}".format(s=SECRET)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')