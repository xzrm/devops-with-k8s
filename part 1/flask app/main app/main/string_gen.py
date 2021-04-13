from flask import Flask
import os
import random
import string
import datetime
import requests
from time import sleep
from concurrent.futures import ThreadPoolExecutor

path = os.path.join('/', 'usr', 'src' ,'app', 'files')
if not os.path.exists(path):
    os.makedirs(path)

file_path = os.path.join(path, 'count.txt')

app = Flask(__name__)

executor = ThreadPoolExecutor(1)

letters = string.ascii_lowercase

logs = []

def generate_random_string():
    while True:
        timestamp = datetime.datetime.utcnow()
        result_str = ''.join(random.choice(letters) for i in range(10))
        log = "{}: {}".format(timestamp, result_str)
        logs.append(log)
        sleep(5)

def read_file(path):
    try:
        with open(path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "File not found"


@app.route('/')
def index():
    # txt = read_file(file_path)
    response = requests.get('http://pong-app-service:8000/count')
    count = response.json()
    try:
        return "<p>{}</p>  <p>Ping / Pong: {}</p>".format(logs[-1], count['count'])
    except IndexError as error:
        return "no logs available"

@app.route('/files')
def get_files():
    files = os.listdir(path)
    return ''.join(files)


if __name__ == '__main__':
    executor.submit(generate_random_string)
    print("starting")
    app.run(debug=True, host='0.0.0.0', use_reloader=False)




