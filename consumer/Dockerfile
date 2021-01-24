FROM python:3.8.7-slim

RUN mkdir -p consumer /data/db
WORKDIR consumer
COPY main.py ./
RUN python3 -m pip install requests==2.25.1

ENTRYPOINT ["python3", "main.py"]