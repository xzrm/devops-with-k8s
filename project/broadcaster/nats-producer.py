import asyncio
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout

async def go(loop):
    nc = NATS()

    try:
        # It is very likely that the demo server will see traffic from clients other than yours.
        # To avoid this, start your own locally and modify the example to use it.
        # await nc.connect(servers=["nats://127.0.0.1:4222"], loop=loop)
        await nc.connect(servers=["nats://localhost:4222"], loop=loop)
    except:
        pass

    async def message_handler(msg):
        print(f"[Received on '{msg.subject}']: {msg.data.decode()}")

    try:
        # Interested in receiving 2 messages from the 'discover' subject.
        # sid = await nc.subscribe("hello", "", message_handler)
        # await nc.auto_unsubscribe(sid, 2)

        await nc.publish("hello", b'hello')
        await nc.publish("hello", b'world')
        await nc.publish("hello", b'again')
        await nc.publish("hello", b'!!!!!')
    except ErrConnectionClosed:
        print("Connection closed prematurely")

    async def request_handler(msg):
        print("[Request on '{} {}']: {}".format(msg.subject, msg.reply,
                                                msg.data.decode()))
        await nc.publish(msg.reply, b'OK')  

    if nc.is_connected:

    #     # Subscription using a 'workers' queue so that only a single subscriber
    #     # gets a request at a time.
        await nc.subscribe("hello", "workers", cb=request_handler)

        try:
            # Make a request expecting a single response within 500 ms,
            # otherwise raising a timeout error.
            msg = await nc.timed_request("hello", b'help please', 0.500)
            print(f"[Response]: {msg.data}")

    #         # Make a roundtrip to the server to ensure messages
    #         # that sent messages have been processed already.
            await nc.flush(0.500)
        except ErrTimeout:
            print("[Error] Timeout!")

    #     # Wait a bit for message to be dispatched...
        await asyncio.sleep(1)

    #     # Detach from the server.
        await nc.close()

    if nc.last_error is not None:
        print(f"Last Error: {nc.last_error}")

    if nc.is_closed:
        print("Disconnected.")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(go(loop))


# import argparse, sys
# import asyncio
# import os
# import signal
# from nats.aio.client import Client as NATS


# async def run(loop):
#     parser = argparse.ArgumentParser()

#     # e.g. nats-pub hello -d "world" -s nats://127.0.0.1:4222 -s nats://127.0.0.1:4223
#     parser.add_argument('subject', default='hello', nargs='?')
#     parser.add_argument('-d', '--data', default="hello world")
#     parser.add_argument('-s', '--servers', default=[], action='append')
#     parser.add_argument('--creds', default="")
#     args = parser.parse_args()

#     nc = NATS()

#     async def error_cb(e):
#         print("Error:", e)

#     async def closed_cb():
#         print("Connection to NATS is closed.")

#     async def reconnected_cb():
#         print(f"Connected to NATS at {nc.connected_url.netloc}...")

#     options = {
#         "loop": loop,
#         "error_cb": error_cb,
#         "closed_cb": closed_cb,
#         "reconnected_cb": reconnected_cb
#     }

#     if len(args.creds) > 0:
#         options["user_credentials"] = args.creds

#     try:
#         if len(args.servers) > 0:
#             options['servers'] = args.servers

#         await nc.connect(**options)
#     except Exception as e:
#         print(e)
#         show_usage_and_die()

#     print(f"Connected to NATS at {nc.connected_url.netloc}...")
#     await nc.publish(args.subject, args.data.encode())
#     await nc.flush()
#     await nc.close()

# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     try:
#         loop.run_until_complete(run(loop))
#     finally:
#         loop.close()