FROM python:3.8.7-slim

RUN mkdir api
WORKDIR api
COPY api.py requirements.txt ./
RUN python3 -m pip install -r requirements.txt

ENTRYPOINT ["python3", "api.py"]