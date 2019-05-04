if [[ ! -a .logged_in_tracker ]]; then
        touch .logged_in_tracker
fi

setopt PROMPT_SUBST
TMOUT=1
TIMEOUT=10
started=$(date +%s -r .logged_in_tracker)

prompt() {
        killall -9 zsh 2>&1 > /dev/null

        left=$((TIMEOUT - `date +%s` + started))
        minutes=`printf "%02d" $((left/60))`
        secs=`printf "%02d" $((left % 60))`

        if [ $left -le 0 ]; then
                echo Goodbye
                exit
        fi

        if [ $left -eq 3 ]; then
                echo -e "You are running out of time to prove you are autonomous.\nPrepare for termination.\n"
        fi

        if [ $left -le 5 ]; then
                color="red"
        elif [ $left -le 7 ]; then
                color="yellow"
        else
                color="green"
        fi

        PROMPT="%B%F%n@%m%f%F{$color}[00:$minutes:$secs]%f:%F{blue}${${(%):-%~}}%f$ %b"
        zle && { zle reset-prompt; zle -R }
}

TRAPALRM() {
        prompt
}

prompt
