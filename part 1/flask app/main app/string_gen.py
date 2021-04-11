from flask import Flask
import os
import random
import string
import datetime
from time import sleep
from concurrent.futures import ThreadPoolExecutor


app = Flask(__name__)

executor = ThreadPoolExecutor(1)

letters = string.ascii_lowercase

logs = []

def generate_random_string():
    while True:
        timestamp = datetime.datetime.utcnow()
        result_str = ''.join(random.choice(letters) for i in range(10))
        log = "{}: {}".format(timestamp, result_str)
        print(log)
        logs.append(log)
        sleep(5)



@app.route('/')
def index():
    try:
        return logs[-1]
    except IndexError as error:
        return "no logs available"


if __name__ == '__main__':
    executor.submit(generate_random_string)
    app.run(debug=True, host='0.0.0.0', use_reloader=False)