##
## if you get a KeyError['product']
## 1) use chrome to log in to Humble Bundle
## 2) navigate to the humble bundle page
## 3) use the getcookies.txt extenstion to dowload the humblebundle.com coookies
## 4) copy the humblebundle.com_cookies.txt file to /mnt/seagatetb
## 5) try again
##

cd ~/humblebundle-downloader
pipenv shell
cd /mnt/seagate8tb

hbd --cookie-file humblebundle.com_cookies.txt --library-path humblebundle.all --keys $1 --progress -p ebook

exit
