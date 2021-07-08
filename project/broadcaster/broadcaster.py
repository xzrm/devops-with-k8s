
import os
import requests
import pika
import time

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

#  https://api.telegram.org/bot<YourBOTToken>/getUpdates
def main():
    sleepTime = 10
    print(' [*] Sleeping for ', sleepTime, ' seconds.')
    time.sleep(sleepTime)

    print('Connecting to server ...')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv("RABBITMQ_URI")))
    channel = connection.channel()
    channel.queue_declare(queue='updates', durable=True)
    print('Waiting for messages.')

    def send_message(message):
        formatted_message = """ ```json {{{message}}}```""".format(message=message)
        send_text = 'https://api.telegram.org/bot' + TELEGRAM_TOKEN + '/sendMessage?chat_id=' + CHAT_ID + '&parse_mode=Markdown&text=' + formatted_message

        response = requests.get(send_text)
        return response.json()

    def callback(ch, method, properties, body):
        print("Received %s" % body)
        send_message(body.decode())
        ch.basic_ack(delivery_tag=method.delivery_tag)


    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='updates', on_message_callback=callback)
    channel.start_consuming()


if __name__ == '__main__':
    main()
