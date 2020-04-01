# System Variables
export PATH="/usr/bin:/bin:/usr/sbin:/sbin" # List of `/etc/paths`
export PATH="/usr/local/bin:$PATH" # Force SSH + brew higher in the path
export PATH="/usr/local/opt/coreutils/libexec/gnubin:$PATH" # override default path with gnutools
export PATH="$HOME/bin:$PATH"
export PATH="$PATH:$HOME/.rvm/bin"
export PATH="$HOME/go/bin:$PATH"
export PATH="$HOME/gocode/bin:$PATH"
export MANPATH="/usr/local/opt/coreutils/libexec/gnuman:$MANPATH"
export code="/Users/tracylivengood/gocode/src/code.uber.internal"

 # No python bytecode
export PYTHONDONTWRITEBYTECODE=1

# Always use go vendoring
export GOPATH=$HOME/gocode

# Add RVM to the path and as a bash function
# export PATH="$PATH:$HOME/.rvm/bin"
# [[ -s "$HOME/.rvm/scripts/rvm" ]] && source "$HOME/.rvm/scripts/rvm"

# Add PYENV to the path
# export PATH="$(pyenv root)/bin:$PATH"
# eval "$(pyenv init -)"

# Add NVM
# export NVM_DIR="$HOME/.nvm"
# [[ -s "$NVM_DIR/nvm.sh" ]] && source "$NVM_DIR/nvm.sh"


# Edit in vim
export EDITOR='vi'

function get_truncated_dir() {
    python ~/code/personal/configuration/truncate-pwd.py $PWD
}

# Handle Colors
export GREP_OPTIONS='--color=auto'
eval "$(dircolors ~/.dircolors)" # depends on dircolor, sets env variables for LS
alias ls='ls -CF --color=auto'	#Print a '/' at end of dirs, a '*' for binaries and a '@' for sym links

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

# Configure and load zsh
export ZSH="/Users/tracylivengood/.oh-my-zsh"
ZSH_THEME="tracy"
plugins=(git)
source $ZSH/oh-my-zsh.sh

