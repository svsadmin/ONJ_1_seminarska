# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 14:06:10 2018

Pridobi URL-je iz arhiva specifične kategorije na strani RTV.si

@author: Admin
"""

import requests
import re
from random import randint
from time import sleep

#RTVSLO - Svet, Politika
url = "http://www.rtvslo.si/svet/arhiv/?&page=0"

#ŠTEVILO STRANI
ST_STRANI = 150

#fo = open("html.txt", "wt")
#print(response.text)
#fo.write(response.text)
#fo.close()

try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

#SHRANJENI URL-JI
fo = open("URL-ji.txt", "wt")

#Poberi URL-je
for i in range(0, ST_STRANI):
    
    querystring = {"page":i}
    response = requests.request("GET", url, params=querystring)
    
    html = response.text
    parsed_html = BeautifulSoup(html, "lxml")
    naslovi = (parsed_html.body.find_all('div', attrs={'class':'listbody'}))
    
    
    for n in naslovi:
        for u in n.find_all('a', href=True):
            print(i)
            if 'https' not in u['href']:
                fo.write(u['href'])
                fo.write('\n')
        

fo.close()
    
