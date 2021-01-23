#!/usr/bin/env python3
import pika
import sys


def callback(ch, method, props, body):
    print(f"[x] Received {body}")


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="hello")
    channel.basic_consume(queue="hello", auto_ack=True, on_message_callback=callback)
    print("[x] Waiting for messages...")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        sys.exit(0)