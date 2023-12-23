##
## if you get a KeyError['product']
## 1) use chrome to log in to Humble Bundle
## 2) navigate to the humble bundle page
## 3) use the getcookies.txt extenstion to dowload the humblebundle.com coookies
## 4) copy the www.humblebundle.com_cookies.txt file to ${HUMBLEBUNDLE_PATH}
## 5) try again
##

cd ~/humblebundle-downloader
HUMBLEBUNDLE_PATH=/mnt/buffalo8tb

pipenv run hbd --cookie-file ${HUMBLEBUNDLE_PATH}/www.humblebundle.com_cookies.txt --library-path ${HUMBLEBUNDLE_PATH}/humblebundle.all --keys $1 --progress -p ebook

exit
