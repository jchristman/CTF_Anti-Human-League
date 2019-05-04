FROM python:3

ENV PWNLIB_NOTERM=true

ARG RUN_AS="dragon"
ARG WORKING_DIR="/dragonctf/babys-second/"

RUN mkdir -p $WORKING_DIR
RUN adduser --quiet --home $WORKING_DIR --gecos "User" $RUN_AS
RUN echo "${RUN_AS}:ALHALWIEUHFLAIWEHF" | chpasswd

WORKDIR $WORKING_DIR
COPY challenge/ .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD [ "python3", "server.py" ]
