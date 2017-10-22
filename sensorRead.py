# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 17:46:17 2017

@author: Aakash
"""
import random

def get_TempHum():
    return random.randrange(23.0,95.0,1),random.randrange(18.0,32,1)

def todegF(degc):
    return (degc*1.8)+32