#!/usr/bin/env python3
import pika
import time
import sys


def main():
    while True:
        time.sleep(2)
        channel.basic_publish(exchange="", routing_key="hello", body="Hello World!")
        print("[x] Sent 'Hello World!'")


if __name__ == "__main__":
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
        channel = connection.channel()
        channel.queue_declare(queue="hello")
        main()
    except KeyboardInterrupt:
        connection.close()
        print("Interrupted")
        sys.exit(0)
