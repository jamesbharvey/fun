#!/bin/bash

#rm -f /mnt/seagate8tb/torrents.done/mycc.indexed
#rm -f /mnt/seagate8tb/torrents.done/index.html

rm -f /mnt/buffalo8tb/torrents.done/mycc.indexed
rm -f /mnt/buffalo8tb/torrents.done/index.html
cd ~/fun/mycc

# set PATH so it includes user's private bin if it exists
if [ -d "$HOME/.local/bin" ] ; then
    PATH="$HOME/.local/bin:$PATH"
fi



pipenv run bin/index.py --production
