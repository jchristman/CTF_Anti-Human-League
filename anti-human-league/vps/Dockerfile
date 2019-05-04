FROM debian:latest

ARG USER_NAME="robot"
ARG USER_PASSWORD="p@$$w0rd"
ARG HOME=/tmp

ENV USER_NAME $USER_NAME
ENV USER_PASSWORD $USER_PASSWORD
ENV CONTAINER_IMAGE_VER=v0.9.0

RUN apt-get update
RUN apt-get install -y \
    sudo curl git-core zsh \
    psmisc procps python3
RUN adduser --quiet --shell /bin/zsh --home $HOME --gecos "User" $USER_NAME
RUN echo "${USER_NAME}:${USER_PASSWORD}" | chpasswd

RUN ln -sf /bin/zsh /bin/sh
RUN rm `which bash`
RUN rm `which dash`

ENV HOME $HOME
WORKDIR $HOME

COPY to_copy/build_haystack.py .
RUN python3 build_haystack.py

COPY to_copy/ .
RUN chmod +x ~/.zshrc
RUN chmod 400 needle
RUN chmod u+s hide_needle

USER $USER_NAME
ENV TERM xterm

CMD [ "zsh" ]
