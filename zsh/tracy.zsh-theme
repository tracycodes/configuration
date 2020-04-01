# See `man zshmisc` for prompt escapes (%)

# Configure git prompt
ZSH_THEME_GIT_PROMPT_PREFIX="%F{default}("
ZSH_THEME_GIT_PROMPT_SUFFIX="%F{default})%f:"
ZSH_THEME_GIT_PROMPT_DIRTY="*"
ZSH_THEME_GIT_PROMPT_CLEAN=""

# Display username in blue
PROMPT='[%F{blue}%n%f:'

# Display git branch, clean or dirty
PROMPT+='$(git_prompt_info)'

# Display time of day in bold
PROMPT+='%B%D{%H:%M:%S}%b:'

# Run python prompt generator to get clean directory
PROMPT+='$(get_truncated_dir)]'

# Display $ prompt, gray on success, red on last command failed.
PROMPT+='%(?.%F{gray}.%F{red})$%f '