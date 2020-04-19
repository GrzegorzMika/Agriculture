FROM arm32v7/python:3.7-buster

RUN mkdir /home/database

COPY . .

WORKDIR /home/database

RUN pip install -r requirements.txt

CMD ["python", "synchronize_gcp.py"]