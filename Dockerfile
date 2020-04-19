# ---- GCP synchronization ----
FROM arm32v7/python:3.7-buster as synchronization

WORKDIR /database

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "synchronize_gcp.py"]