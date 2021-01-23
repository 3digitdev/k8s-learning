FROM python:3.8.7-slim

RUN mkdir api
WORKDIR api
COPY main.py ./
RUN python3 -m pip install fastapi==0.63.0 uvicorn==0.13.3

ENTRYPOINT ["python3", "main.py"]