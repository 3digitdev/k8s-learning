#!/usr/bin/env python3
import os
import requests
import time


def main():
    # These 2 env variables are set in every pod that gets initialized after the FastAPI Service
    url = os.getenv("FASTAPI_SVC_SERVICE_HOST")
    port = os.getenv("FASTAPI_SVC_SERVICE_PORT")
    # Ping for 30 seconds
    for i in range(10):
        response = requests.get(url=f"http://{url}:{port}/hello")
        print(f"http://{url}:{port}/hello [{i+1}] {response.status_code}: {response.json()}")
        time.sleep(3)


if __name__ == "__main__":
    main()
