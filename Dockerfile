FROM raspbian/stretch
FROM arm32v7/python:3.5-buster

RUN apt-get update && \
    apt-get install libpython3.5 -y

RUN echo "deb https://seeed-studio.github.io/pi_repo/ stretch main" | tee /etc/apt/sources.list.d/seeed.list

RUN curl https://seeed-studio.github.io/pi_repo/public.key | apt-key add -

RUN apt-get update && apt install python-mraa python-upm python-rpi.gpio -y

COPY requirements_test.txt /home/pi/database/requirements.txt

RUN pip install -r /home/pi/database/requirements.txt

RUN git clone https://github.com/Seeed-Studio/grove.py

WORKDIR grove.py

RUN pip install .

RUN mkdir /home/pi/logs

WORKDIR /home/pi/database

COPY grove_test.py grove_test.py

CMD python grove_test.py