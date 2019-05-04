#!/bin/bash

IP="127.0.0.1"
URL="http://$IP:5000/vps/new_password"
SECRET="c5368001-70a3-46b4-a2a4-da646b333a75"
USER_NAME="robot"
USER_EXISTS=$(id -u $USER_NAME > /dev/null 2>&1; echo $?)

if [ "$USER_EXISTS" -eq "1" ]; then
	adduser --quiet --home /tmp --gecos "User" $USER_NAME --disabled-password 2>&1 > /dev/null
	usermod -a -G jailed,docker $USER_NAME
fi

NEW_PASSWORD=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)

echo $NEW_PASSWORD
echo $USER_NAME:$NEW_PASSWORD | /usr/sbin/chpasswd

curl -d "new_password=$NEW_PASSWORD&secret=$SECRET" -X POST $URL 2>&1 > /dev/null
