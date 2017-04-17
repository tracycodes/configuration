# System Variables
export PATH="/usr/bin:/bin:/usr/sbin:/sbin" # List of `/etc/paths`
export PATH="/usr/local/bin:$PATH" # Force SSH + brew higher in the path
export PATH="/usr/local/opt/coreutils/libexec/gnubin:$PATH" # override default path with gnutools
export PATH="$HOME/bin:$PATH"
export PATH="$PATH:$HOME/.rvm/bin"
export PATH="$HOME/go/bin:$PATH"
export MANPATH="/usr/local/opt/coreutils/libexec/gnuman:$MANPATH"

# No python bytecode
export PYTHONDONTWRITEBYTECODE=1

# Annoyingly specify the default path for the CA Bundle. Resolves SSL Verify issues.
export SSL_CERT_FILE=/usr/local/etc/openssl/certs/certs.pem

# Always use go vendoring
export GOPATH=$HOME/go

# Add RVM to the path and as a bash function
export PATH="$PATH:$HOME/.rvm/bin"
[[ -s "$HOME/.rvm/scripts/rvm" ]] && source "$HOME/.rvm/scripts/rvm"

# Add PYENV to the path
export PATH="$(pyenv root)/bin:$PATH"
eval "$(pyenv init -)"


# Add NVM
export NVM_DIR="$HOME/.nvm"
[[ -s "$NVM_DIR/nvm.sh" ]] && source "$NVM_DIR/nvm.sh"

# Create a prompt with username + truncated directory + git branch
blue() {
    echo "\[\033[0;34m\]$1\[\033[0m\]"
}
green() {
    echo "\[\033[1;36m\]$1\[\033[0m\]"
}
yellow() {
    echo "\[\033[1;33m\]$1\[\033[0m\]"
}

username=$(blue '\u')
current_time=$(yellow '\t')
export PROMPT_COMMAND='dir=$(python ~/code/personal/configuration/truncate-pwd.py $PWD) &&
                       branch=$(git branch 2> /dev/null | grep "*" | sed "s/* \(.*\)/(\1)/") &&
                       post_branch=$(if [[ "$branch" != "" ]]; then echo $(green $branch):; fi;) &&
                       export PS1="[$username:$post_branch$current_time:$dir]$ "'

# Edit in Sublime
export EDITOR='vi'

#If ambiguous files are available, list them with each tab press (one instead of two)
bind "set show-all-if-ambiguous on"

#Ignore case when tab completeing
bind "set completion-ignore-case on"

# Use git completion
if [ -f `brew --prefix`/etc/bash_completion ]; then
    . `brew --prefix`/etc/bash_completion
fi

# Improve bash history
export HISTFILESIZE=99999
export HISTSIZE=$HISTFILESIZE
export HISTTIMEFORMAT='%F %T '

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
alias unmount="diskutil diskutil unmountDisk force"

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

## Convenient Functions

filesize() {
	ls -l $*
	ls -lt $* | awk '{kb += $5} END {kb=kb/1024 ; printf(" TOTAL SIZE: %4.2f MB\n",kb/1024)}'
}

# Find files
f() {
    find . -name $1
}

# Find files and search them for content
# fg() {
#     find . -name $1 -exec grep -iHn $2 {} \;
# }

# Find files and structure as a tree -- TSL Doesn't work for some reason
ft() {
    tree --prune -P $1
}

# Find files and paths and search them for content
fwg() {
    find . -name $1 -and -wholename $2 -exec grep -iHn $3 {} \;
}

# Kill
k() {
    sudo kill `ps aux | grep $1 | awk '{print $2}'`
}

# Find files with a certain name and remove them (with prompt)
fr() {
    find . -name $1 -exec rm -i {} \;
}

clean_pycache() {
     sudo find . -name __pycache__ -exec rm -r {} +
}

# All of these lsof commands use -P to prevent port number conversion to names
services() {
    lsof -iTCP -P
}

local_services() {
    lsof -iTCP@localhost -P
}

process_services() {
    lsof -p $1 -P
}

check_port() {
    lsof -i :$1 -P
}

build_ctags() {
    find . -not \( -ipath "./.git*" -o -ipath "./thumbprint/_build/*" -o -ipath "./thumbprint/node_modules/*" -o -ipath "./public/_assets/*" -o -ipath "./vendor*"  \) | ctags -L -
}

