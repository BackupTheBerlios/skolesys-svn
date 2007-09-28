umask 022

export PATH="/bin:/usr/bin:/sbin:/usr/sbin:$PATH:/usr/X/bin:/usr/local/bin"

setopt extendedhistory

# Prompt
PROMPT=$'%{\e[1;32m%}%T%{\e[0m%} %n@%m% %{\e[0m%} %? %# ';
RPROMPT=' %~'; # prompt for right side of screen

alias ls='ls --color=auto';
alias which='type'
alias mc='mc -cu'
alias mv='nocorrect mv'       # no spelling correction on mv
alias cp='nocorrect cp'       # no spelling correction on cp
alias mkdir='nocorrect mkdir' # no spelling correction on mkdir
alias mail='Mail'
alias l='ls -F'
alias ll='ls -lF'
alias lla='ls -laF'
alias la='ls -laF'
alias lld='ls -ld *(-/DN)'
alias lsd='ls -d *(-/DN)'
alias lsa='ls -ld .*'
alias gnus='export TERM=linux;nano -f gnus'

# The following lines were added by compinstall
autoload -U compinit
compinit


zstyle ':completion:*' completer _expand _complete _correct
zstyle ':completion:*' format 'Complete %d'
zstyle ':completion:*' list-colors ${(s.:.)LS_COLORS}
zstyle ':completion:*' list-prompt %SAt %p: Hit TAB for more, or the character to insert%s
zstyle ':completion:*' select-prompt '%SScrolling active: current 
selection at %p%s'

zstyle ':completion:*' matcher-list 'm:{a-z}={A-Z} m:{a-zA-Z}={A-Za-z}' '' '' 'r:|[._-]=* r:|=*'
zstyle ':completion:*' max-errors 1
zstyle ':completion:*' menu select=5
zstyle ':completion:*' prompt 'Liste'
zstyle ':complete:*:history-words' stop verbose

# End of lines added by compinstall


# Variabel settings
export PAGER="less"
export MANPAGER="$PAGER"
export EDITOR="nano"
export TERM="xterm"
export EDIT="$EDITOR"
export VISUAL="$EDITOR"
export PILOTRATE="115200"
export LS_COLORS='no=00:fi=00:di=01;34:ln=01;36:pi=40;33:so=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arj=01;31:*.taz=01;31:*.lzh=01;31:*.zip=01;31:*.z=01;31:*.Z=01;31:*.gz=01;31:*.bz2=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.jpg=01;35:*.png=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.png=01;35:*.mpg=01;35:*.avi=01;35:*.fli=01;35:*.gl=01;35:*.dl=01;35:'

HISTSIZE="5000"
HISTFILE="${HOME}/.zsh_history"
SAVEHIST="2000"
