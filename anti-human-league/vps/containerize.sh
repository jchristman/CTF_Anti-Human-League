#!/bin/sh

containerize()
{
    (sleep 11 && echo && echo && echo Somehow you managed to escape the timeout. This means you are human and your session is now terminated... && echo && echo) &
    (sleep 12 && docker ps | grep anti-human-league-vps | grep -v "Up [0-9] second" | awk '{print $1}' | xargs docker kill) 2>&1 > /dev/null &
    docker run --rm $1 \
               --hostname robot-vps \
               power-programming:anti-human-league-vps zsh
}

# Check if TTY allocated
if tty -s; then
    containerize -it
else
    containerize -i
fi
