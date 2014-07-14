#Set prompt '[username]:[pwd]$'
export PS1="[\u:\w]$ "

#Truncate path in prompt to three directories
export PROMPT_DIRTRIM=3

#No Beeping.
setterm -blength 0

#If ambiguous files are available, list them with each tab press (one instead of two)
bind "set show-all-if-ambiguous on"

#Ignore case when tab completeing
bind "set completion-ignore-case on"

# Use git completion
if [ -f ~/.git-completion.sh ]; then
	source ~/.git-completion.sh
fi

# Improve bash history
export HISTFILESIZE=99999
export HISTSIZE=$HISTFILESIZE
export HISTTIMEFORMAT='%F %T '
shopt -s cmdhist
shopt -s histappend

# Forgive mistakes
shopt -s cdspell
shopt -s dirspell

# Convenience Aliases
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'
alias .....='cd ../../../..'

# Patching and Diffing CVS
alias cvsc='cvs up 2>&1 | grep --color "U \|P \|A \|R \|M \|C \|? "'
alias cvsdp='cvs -q diff -up > ~/patch'
alias pd='patch -N -p0 --dry-run < ~/patch'
alias p='patch -N -p0 < ~/patch'

# Handle Colors
export GREP_OPTIONS='--color=auto'
eval "$(dircolors ~/.dircolors)" # depends on dircolor, sets env variables for LS
alias ls='ls -CF --color=auto'	#Print a '/' at end of dirs, a '*' for binaries and a '@' for sym links
alias ll='ls --color=auto -lh'

# Let GRC colorize some useful tools
GRC=`which grc`
if [ "$TERM" != dumb ] && [ -n "$GRC" ]
then
    alias colourify="$GRC -es --colour=auto"
    alias configure='colourify ./configure'
    alias diff='colourify diff'
    alias make='colourify make'
    alias gcc='colourify gcc'
    alias g++='colourify g++'
    alias as='colourify as'
    alias gas='colourify gas'
    alias ld='colourify ld'
    alias netstat='colourify netstat'
    alias ping='colourify ping'
    alias traceroute='colourify /usr/sbin/traceroute'
fi

# System Variables....should likely import per system.
PATH=$PATH:$HOME/bin

# Convenient Functions
filesize() {
	ls -l $*
	ls -lt $* | awk '{kb += $5} END {kb=kb/1024 ; printf(" TOTAL SIZE: %4.2f MB\n",kb/1024)}'
}

# find file, find content, find content and replace, etc.