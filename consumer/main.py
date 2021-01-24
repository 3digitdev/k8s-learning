#!/usr/bin/env python3
import os
import requests
import time

DATA_FILE = "/data/db/out.txt"


def main():
    # These 2 env variables are set in every pod that gets initialized after the FastAPI Service
    url = os.getenv("FASTAPI_SVC_SERVICE_HOST")
    port = os.getenv("FASTAPI_SVC_SERVICE_PORT")
    # Don't change the behavior for old Goals
    use_file = os.getenv("USE_DATA_FILE") is not None
    # Clear out the file so when the Pod restarts, it doesn't just keep appending
    if use_file:
        with open(DATA_FILE, "w") as df:
            df.write("")
    # Ping for 10 seconds
    for i in range(10):
        response = requests.get(url=f"http://{url}:{port}/hello")
        out = f"http://{url}:{port}/hello [{i+1}] {response.status_code}: {response.json()}\n"
        if use_file:
            with open(DATA_FILE, "a") as df:
                df.write(out)
        else:
            print(out)
        time.sleep(1)
    if use_file:
        with open(DATA_FILE, "r") as df:
            print("Data File\n---------")
            for line in df.readlines():
                if line != "\n":
                    print(line.strip("\n"))


if __name__ == "__main__":
    main()
