FROM python:3

ENV PWNLIB_NOTERM=true

ARG RUN_AS="dragon"
ARG WORKING_DIR="/dragonctf/anti-human-league/"

RUN mkdir -p $WORKING_DIR
RUN adduser --quiet --home $WORKING_DIR --gecos "User" $RUN_AS
RUN echo "${RUN_AS}:ALHALWIEUHFLAIWEHF" | chpasswd

WORKDIR $WORKING_DIR
RUN pip install --upgrade pip
COPY website/requirements.txt .
RUN pip install -r requirements.txt
RUN pip install gunicorn

RUN apt-get update
RUN apt-get install sqlite3 -y

COPY website/ .

RUN ./init.sh

# gunicorn -b 0.0.0.0:5000 server:app
CMD [ "gunicorn", "--workers=3", "-b", "0.0.0.0:5000", "server:app" ]
