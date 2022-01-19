#!/bin/bash
sudo mount -t cifs -o rw,vers=2.0,credentials=/home/pi/.shield_credentials  //192.168.11.7/internal /mnt/shield
