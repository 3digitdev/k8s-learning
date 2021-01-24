import json
import uvicorn

from fastapi import FastAPI

DATA_FILE = "/data/db/stuff.json"
app = FastAPI()


@app.get("/hello")
async def root():
    with open(DATA_FILE, "r") as df:
        data = json.load(df)
    return data


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
