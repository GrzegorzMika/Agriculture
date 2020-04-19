# ---- GCP synchronization ----
FROM arm32v7/python:3.7-buster as synchronization

RUN mkdir -p /home/database

COPY . /database

WORKDIR /database

RUN pip install -r requirements.txt

CMD ["python", "synchronize_gcp.py"]