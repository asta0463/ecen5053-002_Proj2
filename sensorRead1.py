# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 17:30:24 2017

@author: Aakash
"""

import Adafruit_DHT

sensor = Adafruit_DHT.DHT22
pin = 4

def get_TempHum():
    return Adafruit_DHT.read_retry(sensor, pin)

def todegF(degc):
    return (degc*1.8)+32