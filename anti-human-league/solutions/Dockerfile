FROM python:3

ENV PWNLIB_NOTERM=true

ARG RUN_AS="dragon"
ARG WORKING_DIR="/dragonctf/anti-human-league/solutions"

RUN mkdir -p $WORKING_DIR
RUN adduser --quiet --home $WORKING_DIR --gecos "User" $RUN_AS
RUN echo "${RUN_AS}:ALHALWIEUHFLAIWEHF" | chpasswd
RUN apt-get update
RUN apt-get install tesseract-ocr -y

WORKDIR $WORKING_DIR
COPY solutions/requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY solutions/ .

CMD [ "/bin/bash" ]
