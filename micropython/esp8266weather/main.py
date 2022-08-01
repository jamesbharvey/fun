import dht
import network
import socket

from time import sleep
from machine import Pin

sensor = dht.DHT11(Pin(5))


secrets_file = open("wifisecrets.txt",'r')
first_line = secrets_file.readline()
ssid, password = first_line.split()
secrets_file.close()

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(ssid, password)

last_sent_time = 0
UDP_PORT = 2004
UDP_IP = "192.168.11.23"


def send_udp(message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.sendto(bytes(message, "utf-8"), (UDP_IP, UDP_PORT))


def send_to_graphite(temp, humi):
    temp_message = "mysensors.kitchen.temperature %3.1f -1" % temp
    humi_message = "mysensors.kitchen.humidity %3.1f -1" % humi
    send_udp(temp_message)
    sleep(1)
    send_udp(humi_message)


while True:
    try:
        while not sta_if.isconnected():
            print("retry connecting to file ssid[%s]" % ssid)
            sta_if.connect(ssid, password)
            sleep(30)
        sensor.measure()
        t = sensor.temperature()
        h = sensor.humidity()
        print('Temperature: %3.1f C' % t)
        print('Humidity: %3.1f %%' % h)
        send_to_graphite(t, h)
        sleep(28)

    except OSError as e:
        print('Sensor Reading Failed')
