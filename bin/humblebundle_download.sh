
cd ~/humblebundle-downloader
pipenv shell
cd /mnt/seagate8tb

hbd --cookie-file humblebundle.com_cookies.txt --library-path humblebundle.all --keys XXXXX --progress -p ebook
