#!/bin/bash

#rm -f /mnt/seagate8tb/torrents.done/mycc.indexed
#rm -f /mnt/seagate8tb/torrents.done/index.html

rm -f /mnt/buffalo8tb/torrents.done/mycc.indexed
rm -f /mnt/buffalo8tb/torrents.done/index.html
cd ~/fun/mycc


pipenv run bin/index.py --production
