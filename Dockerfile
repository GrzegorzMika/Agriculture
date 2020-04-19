# ---- GCP synchronization ----
FROM arm32v7/python:3.7-slim as synchronization

RUN apt-get update

COPY requirements.txt /database/requirements.txt

RUN pip install -r /database/requirements.txt

COPY . /database

CMD ["python", "/database/synchronize_gcp.py"]