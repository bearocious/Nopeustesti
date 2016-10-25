#!/usr/bin/env python
# -*- coding: utf8 -*-
__version__ = '0.1'
__author__ = 'Gabriel Kinkela'

import time
import random
import threading
import os
from getch import getch, pause
import CHIP_IO.GPIO as GPIO

hiparit = 5
nappiJono = [] #Napit joita pelaajan täytyy painaa järjestyksessä
peliNopeus = 1
lediPaalla = 1
lediMaara = 4
playerPressed = 0
peli = False
teksti = "Pisteet: "
pisteet = 0


#Alustetaan ledit
GPIO.cleanup()
sin = GPIO.setup("XIO-P2", GPIO.OUT)
kel = GPIO.setup("XIO-P3", GPIO.OUT)
pun = GPIO.setup("XIO-P4", GPIO.OUT)
vih = GPIO.setup("XIO-P5", GPIO.OUT)
ledit = [sin,kel,pun,vih]

#Asetetaan haluttu ledi päälle
def lediPaalle (mikaledi):
	GPIO.output("XIO-P" + str(mikaledi + 1), 0)
	return None

#Asetetaan haluttu ledi kiinni
def lediKiinni (mikaledi):
	GPIO.output("XIO-P" + str(mikaledi + 1), 1)
	return None

#Asettaa halutun ledin päälle ja lisää sen pelaajan painettavien nappien jonoon
def asetaLedi (mikaledi):
	#Lisätään jonon alkuun haluttu ledi ja laitetaan se päälle
	nappiJono[len(nappiJono):] = [mikaledi]
	edellinen = nappiJono[-1]
	lediPaalle(mikaledi)
	
	#Jos sama ledi valitaan kahdesti niin väläytetään sitä
	if(edellinen == mikaledi):
		lediKiinni(mikaledi)
		time.sleep(peliNopeus / 5)
		lediPaalle(mikaledi)

	#Kytketään muut ledit pois päältä
	mones = 0
	for ledi in range(lediMaara):
		mones += 1
		if (mones != mikaledi):
			lediKiinni(mones)

	return None

#Asetetaan satunnainen ledi päälle
def teeJono():
	while(peli):
		x = random.randint(1, 4)
		if (x == 1):
			asetaLedi(1)
		elif (x == 2):
			asetaLedi(2)
		elif (x == 3):
			asetaLedi(3)
		elif (x == 4):
			asetaLedi(4)
		else:
			print("Virhe!")
		time.sleep(peliNopeus)
	return None


if (peli == False):
	os.system('clear')
	peliNopeus = float(raw_input("Valitse nopeus: ")) #Pyydetään pelaajalta nopeutta
	t = threading.Timer(peliNopeus, teeJono) #Asetetaan ja käynnistetään ajastin
	teeJono()
	t.start()
	peli = True

#Päälooppi
while(hiparit > 0):
	try:
		ch = int(getch())
	except:
		peli = False
		t.cancel()
		exit()
	if(ch == nappiJono[0]):
		nappiJono.pop(0)
		pisteet += 1
		os.system('clear')
		print("Pisteet: " + str(pisteet))
	else:
		peli = False
		t.cancel()
		exit()
