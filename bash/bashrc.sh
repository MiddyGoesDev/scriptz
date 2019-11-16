#add libraries to path
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}

# add to pythonpath
export PYTHONPATH=/usr/local/cuda-9.0/lib64${PYTHONPATH:+:${PYTHONPATH}}

# add folders to path:
PATH=/informatik2/students/home/5rietz/pycharm-2019.1.3/bin${PATH:+:${PATH}}
PATH=/usr/local/cuda-9.0/bin${PATH:+:${PATH}}

# for uhh vpn
# https://www.rrz.uni-hamburg.de/services/netz/vpn/vpn-linux.html
alias univpn="/opt/cisco/anyconnect/bin/vpnui"

# anaconda navigator
alias nav="anaconda-navigator"

# color ls ouput
alias ls="ls --color=auto"

# color grep output
alias grep="grep --color=auto"

# gac "commit message"
alias gac="git add . && git commit -a -m "

# echo ip of machine
alias myip="curl http://ipecho.net/plain; echo"

# sort by size all files in human readable format
alias lss="ls -Ssha --color=auto"

# -a archive mode: preserve permissions, ownership, edit times etc
# -v verbose output
# -z compression during transer
# -h humanm readable output
# --info=progress2 total progres percentage
alias rsync="rsync -avzh --info=progress2"

# use find to delete all files in all subdirectories with the given name
fd() {
        if [ $# -eq 1 ]
        then
                echo "Deleting files containing '$1' from all subdiretories...";
                find . -name "$1" -type f -delete -print;
                echo "Done";
        else
                echo "FAIL: Provide a non-empty string parameter to determine which files to delete";
        fi
}

