
import asyncio
import os
import signal
from nats.aio.client import Client as NATS
import requests
import os
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

#  https://api.telegram.org/bot<YourBOTToken>/getUpdates

def send_message(message):
    # message = """*bold text*\n```json { \n "some": "json", \n "some": "json", \n "some": { "some": "json" }"\n}```"""
    formatted_message = """*bold text* ```json {{{message}}}```""".format(message=message)

    send_text = 'https://api.telegram.org/bot' + TELEGRAM_TOKEN + '/sendMessage?chat_id=' + CHAT_ID + '&parse_mode=Markdown&text=' + formatted_message

    response = requests.get(send_text)
    return response.json()


async def run(loop):

    nc = NATS()

    async def error_cb(e):
        print("Error:", e)

    async def closed_cb():
        print("Connection to NATS is closed.")
        await asyncio.sleep(0.1, loop=loop)
        loop.stop()

    async def reconnected_cb():
        print(f"Connected to NATS at {nc.connected_url.netloc}...")

    async def subscribe_handler(msg):
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()

        print("Received a message on '{subject} {reply}': {data}".format(
          subject=subject, reply=reply, data=data))
        send_message(data)

    options = {
        "servers": [os.getenv("NATS_URI")],
        "loop": loop,
        "error_cb": error_cb,
        "closed_cb": closed_cb,
        "reconnected_cb": reconnected_cb
    }

    try:
        await nc.connect(**options) 
    except Exception as e:
        print(e)

    print(f"Connected to NATS at {nc.connected_url.netloc}...")
    
    def signal_handler():
        if nc.is_closed:
            return
        print("Disconnecting...")
        loop.create_task(nc.close())

    for sig in ('SIGINT', 'SIGTERM'):
        loop.add_signal_handler(getattr(signal, sig), signal_handler)

    await nc.subscribe("updates", "", subscribe_handler)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
    try:
        loop.run_forever()
    finally:
        loop.close()