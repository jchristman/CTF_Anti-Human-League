#!/bin/bash

echo Cleaning old databases
rm *.db

echo
echo Initializing databases
FLASK_APP=practice1/main.py flask initdb
FLASK_APP=practice2/main.py flask initdb
FLASK_APP=blog/main.py flask initdb
FLASK_APP=vpspractice/main.py flask initdb
FLASK_APP=vps/main.py flask initdb

echo
echo Populating databases
sqlite3 blog.db ".read init.sql"
