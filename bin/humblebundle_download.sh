
source ~/humbledownload.env/bin/activate

cd /mnt/stick8tb
hbd --cookie-file cookies.txt --update --library-path humblebundle.all --progress -p ebook
# hbd --cookie-file /mnt/stick8tb/humblebundle.com_cookies.txt --library-path humblebundle.all --keys XXXXX --progress -p ebook
