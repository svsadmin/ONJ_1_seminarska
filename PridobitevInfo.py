# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 11:28:24 2018

@author: Admin
"""

import requests
import re
from random import randint
from time import sleep
import pickle
import codecs
try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup
from os import listdir
from os.path import isfile, join

def pridobiDrzave():

    #url = "http://www.gu.gov.si/fileadmin/gu.gov.si/pageuploads/PROJEKTI/Registri/KSZI/abecedni.html"
    #response = requests.request("GET", url)
    
    #html = response.text
    #print(html)
    #html = ". ".join(html.split("<br />"))
    html = codecs.open("drzave.html", "r", "utf-8")
    parsed_html = BeautifulSoup(html, "lxml")
    tabele = parsed_html.body.find_all('td')
    #print(tabele)


    drzave = {}
    splosne_besede = ["republika", "obala", "otoki", "velika"]

    for idx, val in enumerate(tabele):
        if ((idx > 3) and (idx % 3 == 0)):
            text = val.get_text()
            if text[-1] == " ":
                text = text[:-1]
            if (len(text) > 2):
                for s in text.split(" "):
                    if (s.lower() not in splosne_besede):
                        drzave[s] = text

    drzave["ZDA"] = "Združene države Amerike"
    drzave["ZAE"] = "Združeni arabski emirati"
    drzave["JAR"] = "Južna Afrika"
    drzave["Južnoafriška republika"] = "Južna Afrika"
    drzave["Britanija"] = "Velika Britanija"
    
    with open("drzave.txt", "wb") as fp:
        pickle.dump(drzave, fp)
    
    return drzave 
        
def pridobiPridevnike():
    
    urls = ["https://sl.wiktionary.org/w/index.php?title=Kategorija:Slovenski_pridevniki",
            "https://sl.wiktionary.org/w/index.php?title=Kategorija:Slovenski_pridevniki&pagefrom=konservativen#mw-pages",
            "https://sl.wiktionary.org/w/index.php?title=Kategorija:Slovenski_pridevniki&pagefrom=podzemski#mw-pages",
            "https://sl.wiktionary.org/w/index.php?title=Kategorija:Slovenski_pridevniki&pagefrom=uvo%C5%BEen#mw-pages"]
    
    fileObj = codecs.open("pridevniki", "w", "utf-8" )
    for url in urls:
        response = requests.request("GET", url)
        html = response.text
        html = ". ".join(html.split("<br />"))
        parsed_html = BeautifulSoup(html, "lxml")
        vse = parsed_html.body.find_all('div', attrs={'class':'mw-category'})
        
        pridevniki = []
        for v in vse:
            for pridevnik in v.find_all('li'):
                fileObj.write(pridevnik.get_text() + "\n")
    fileObj.close()
