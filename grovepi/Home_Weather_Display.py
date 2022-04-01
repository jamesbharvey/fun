#!/usr/bin/env python3

# Home_Weather_Display.py
#
# This is an project for using the Grove RGB LCD Display and the Grove DHT Sensor from the GrovePi starter kit
#
# In this project, the Temperature and humidity from the DHT sensor is printed on the RGB-LCD Display
#
#
# Note the dht_sensor_type below may need to be changed depending on which DHT sensor you have:
#  0 - DHT11 - blue one - comes with the GrovePi+ Starter Kit
#  1 - DHT22 - white one, aka DHT Pro or AM2302
#  2 - DHT21 - black one, aka AM2301
#
# For more info please see: http://www.dexterindustries.com/topic/537-6c-displayed-in-home-weather-project/
#

from grovepi import *
from grove_rgb_lcd import *
from time import sleep
from math import isnan
from time import localtime, strftime
import socket

dht_sensor_port = 2 # connect the DHt sensor to port 7
dht_sensor_type = 0 # use 0 for the blue-colored sensor and 1 for the white-colored sensor
last_sent_time = 0
UDP_PORT = 2004
UDP_IP = "192.168.11.23"

# set green as backlight color
# we need to do it just once
# setting the backlight color once reduces the amount of data transfer over the I2C line
setRGB(0,255,0)
setText("")

def send_udp(message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sock.sendto(bytes(message, "utf-8"), (UDP_IP, UDP_PORT))

def send_to_graphite(temp,humi):
    temp_message = "mysensors.study.temperature " + temp + " -1"
    humi_message = "mysensors.study.humidity " + humi + " -1"
    send_udp(temp_message)
    send_udp(humi_message)
    
    
while True:
    try:
        # get the temperature and Humidity from the DHT sensor
        [ temp,hum ] = dht(dht_sensor_port,dht_sensor_type)
#        print(strftime("%Y-%b-%d %H:%M:%S",localtime()))
#        print( temp, "C ", hum,"% Hum.\t")


        # check if we have nans
        # if so, then raise a type error exception
        if isnan(temp) is True or isnan(hum) is True:
            raise TypeError('nan error')

        t = str(temp)
        h = str(hum)

        # instead of inserting a bunch of whitespace, we can just insert a \n
        # we're ensuring that if we get some strange strings on one line, the 2nd one won't be affected
        setText_norefresh(strftime("%b %d %H:%M",localtime())
        + "\n" + t + "C " +  h + "% Hum")

        if (time.time() - last_sent_time) > 30:
#           print("send packet")
            last_sent_time = time.time()
            send_to_graphite(t,h)
#        else:
#            print("don't send packet")

    except (IOError, TypeError) as e:
        print(str(e))
        # and since we got a type error
        # then reset the LCD's text
        setText("")

    except KeyboardInterrupt as e:
        print(str(e))
        # since we're exiting the program
        # it's better to leave the LCD with a blank text
        setText("")
        break

    # wait some time before re-updating the LCD
    sleep(5)
