#!/bin/bash

echo
echo ======================= Babys First Script Setup =======================

cd babys-first-script
./build.sh
./run.sh

echo
echo ======================= Babys Second Script Setup =======================

cd ../babys-second-script
./build.sh
./run.sh

echo
echo ======================= Anti-Human-League Setup =======================

cd ../anti-human-league
./build.sh
./run.sh

echo
echo ======================= Anti-Human-League VPS Setup =======================
cd vps

echo -------------------------
echo Building docker container
./build.sh

echo 
echo ------------------------------
echo Installing containerize script
cp -f containerize.sh /usr/local/containerize.sh

echo
echo ======================= Summary =======================

echo
echo -------------------------------------
echo Add the following to your sshd_config

echo
echo vim /etc/ssh/sshd_config
echo
echo Match Group jailed
echo "      ForceCommand /usr/local/containerize.sh"
echo "      PasswordAuthentication yes"
echo "      AllowTcpForwarding no"
echo "      PermitTunnel no"
echo "      X11Forwarding no"

echo
echo -------------------------------------
echo "Enter the below commands to create the cron job to create the user \"robot\" and change his password randomly every minute. NOTE: change the IP in change-password.sh for production"

echo
echo crontab -e
echo \* \* \* \* \* `pwd`/change-password.sh

echo
echo There is a little manual setup required for the VPS. Complete the steps between the Summary line and here.
echo Solutions are in a docker container at anti-human-league/solutions.
echo
echo cd anti-human-league/solutions
echo ./build.sh
echo ./run.sh
