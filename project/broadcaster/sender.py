
from flask import (
    Flask
)

import asyncio
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout


app = Flask(__name__)
# loop = asyncio.get_event_loop()


@app.route('/test')
async def test_nats():
    # asyncio.set_event_loop(asyncio.new_event_loop())
    # loop =asyncio.new_event_loop()
    # loop = asyncio.get_event_loop()
    # await hello()
    await hello()
    # loop.run_until_complete(hello(loop)) 
    return 'Hello world !'

@app.route('/')
async def index():
    return 'hi'

# async def hello():
#     await asyncio.sleep(5)
#     return 1
async def hello():
    loop = asyncio.get_event_loop()
    nc = NATS()
    try:
        await nc.connect(servers=["nats://localhost:4222"], loop=loop)
    except:
        pass

    try:
        await nc.publish("updates", b'hello')
        await nc.publish("updates", b'world')
    except ErrConnectionClosed:
        print("Connection closed prematurely")

    if nc.is_connected:
        await nc.close()

    if nc.is_closed:
        print("Disconnected.")
    return 1

if __name__ == "__main__":
    app.run()