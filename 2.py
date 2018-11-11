# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 14:52:40 2018

@author: Admin
"""

import requests
import re
from random import randint
from time import sleep
import pickle

#Osnovni URL
url_osnovni = "http://www.rtvslo.si"

#Prenesi shranjene URL-je
fo = open("URL-ji.txt", "rt")

#Tabela člankov
clanki = []

#Tabela pripadajočih datumov
datumi = []

try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

i = 0
#Pridobi članke in jih shrani v seznam
for u in fo:
    i+=1
    t = ''
    url = url_osnovni + u.rstrip() + "/"
    
    print("Pridobivam novico na naslovu:" + url)
    
    response = requests.request("GET", url)
    
    html = response.text
    
    #Odstrani lomljenja vrstic
    html = ". ".join(html.split("<br />"))
    parsed_html = BeautifulSoup(html, "lxml")
    novica = (parsed_html.body.find_all('div', attrs={'id':'newsbody'}))
    
    datum = (parsed_html.body.find_all('div', attrs={'class':'info'}))
    
    for n in novica:
        #najdi datum
        for odstavek in n.find_all('div', attrs={'class':'info'}):
            d = odstavek.get_text().strip().split(" ")
            datum = '_'.join(d[:3])
            datumi.append(datum)
        
        #najdi vsebino
        for odstavek in n.find_all('p'):
            if (odstavek.get_text()[-1:] != ' '):
                t+=(odstavek.get_text() + ' ')
            else:
                t+=odstavek.get_text()
                
    clanki.append(t)
    
    try:    
        link = './clanki/' + str(i) + '_' + str(datum) + '.txt'  
        ff = open(link, 'w', encoding='utf-8')
        ff.write(t)
        ff.close()
    except:
        link = './clanki/' + str(i) + '____________' + '.txt'
    
with open("clanki.txt", "wb") as fp:
    pickle.dump(clanki, fp)

with open("datumi.txt", "wb") as fd:
    pickle.dump(datumi, fd)