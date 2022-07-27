#!/bin/bash

cd RTL8812BU
make
# don't worry about this -
#Skipping BTF generation for /home/james/src/RTL8812BU/88x2bu.ko due to unavailability of vmlinux
#
sudo make install
sudo reboot

exit
#make clean && make && sudo make install && sudo reboot

#sudo modprobe 88x2bu

# clone the new branch:
# sudo apt update
# sudo apt install -y dkms git bc
# git clone -b v5.8.7 https://github.com/fastoe/RTL8812BU.git
# cd RTL8812BU
# make
# # don't worry about this -
# #Skipping BTF generation for /home/james/src/RTL8812BU/88x2bu.ko due to unavailability of vmlinux
# #
# sudo make install
# sudo reboot
# make clean && make && sudo make install && sudo reboot

# sudo modprobe 88x2bu
