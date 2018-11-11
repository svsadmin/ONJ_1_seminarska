# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 20:06:11 2018

@author: Admin
"""

import codecs
import pickle
import operator
try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup
from os import listdir
from os.path import isfile, join


class LematiziranaBeseda:
    def __init__(self, lemma, oznaka, osnovna, datum):
        self.lemma = lemma
        self.oznaka = oznaka
        self.osnovna = osnovna
        self.datum = datum

def najdiBias(kljuci):
    fileObj = codecs.open("bias_pridevniki.txt", "r", "utf-8")
    
    #pridevniki in njihova +/- nagnjenost. Skupni bias pomeni seštevek pridevnikov
    bias = {}
    skupniBias = 0
    vsiPridevniki = 0
    rezultat = []
    
    for f in fileObj:
        bias[f[:-2]] = f[-2]
    
    for i in range(0, len(kljuci)):
        if (kljuci[i][0] in bias.keys()):
            if (bias[kljuci[i][0]] == '+'):
                skupniBias += kljuci[i][1]
                vsiPridevniki += kljuci[i][1]
            else: 
                skupniBias -= kljuci[i][1]
                vsiPridevniki += kljuci[i][1]
            
            rezultat.append(kljuci[i][0] + " " + str(bias[kljuci[i][0]]) + " " + str(kljuci[i][1]))
    
    skupniBias = skupniBias/vsiPridevniki
    return rezultat, skupniBias

def najdiIdeologijo(kljuci):
    fileObj = codecs.open("politicni_pridevniki.txt", "r", "utf-8")
    
    #politicni pridevniki
    politicni = []
    
    for f in fileObj:
        politicni.append([f[:-1], 0])
    
    for i in range(0, len(kljuci)):
        for j in range(0, len(politicni)):
            #Če se samostalnik konča na -ist, se pridevnik na -ističen
            if (politicni[j][0][-3:] == "ist"):
                if ((politicni[j][0] == kljuci[i][0]) or ((politicni[j][0] + "ičen") == kljuci[i][0])):
                    politicni[j][1] += 1
            #Če se samostalnik konča na -ec se pridevnik na -en
            elif (politicni[j][0][-2:] == "ec"):
                if ((politicni[j][0] == kljuci[i][0]) or ((politicni[j][0][-1] + "n") == kljuci[i][0])):
                    politicni[j][1] += 1
            else:
                if politicni[j][0] == kljuci[i][0]:
                    politicni[j][1] += 1
                    
    return sorted([(politicni[i][0], politicni[i][1]) for i in range(len(politicni)) if politicni[i][1] > 0], key = lambda x: x[1], reverse = True)[0:3]

def najdiDrzavo(kljuci):
    with open("drzave.txt", "rb") as fp:
        drzave = pickle.load(fp)
        drzave_st = {drzave[drz]:0 for drz in drzave.keys()}
        
        #Iskanje najbolj podobne države glede na prvih n črk ter dodelitev točk
        for kljuc in kljuci:
            for drz in drzave.keys():
                
                idx_s = 0
                vsota = 0
                k = kljuc[0].lower()
                d = drz.lower()
                
                #Sklepamo, da gre za pridevnik
                if ((k[-3:] == "ški") or (k[-3:] == "ski") or (k[-2:] == "ec")):
                    #print(k)
                    #print(d)
    
                    while (k[idx_s] == d[idx_s]):
                        if ((idx_s + 1) < len(k) and (idx_s + 1) < len(d)):
                            idx_s += 1
                        else:
                            break
                        vsota += 1
                    
                    if (vsota >= 3):
                        drzave_st[drzave[drz]] += ((vsota + kljuc[1])/3)
                    
                if k == d:
                    drzave_st[drzave[drz]] += kljuc[1]
        
        return sorted(drzave_st.items(), key=operator.itemgetter(1), reverse=True)

def najdiIme(kljuci, oznake):
    with open("drzave.txt", "rb") as fp:
        drzave = pickle.load(fp)
        
        politikiFile = codecs.open("politiki2.txt", "r", "utf-8")
        politiki = [p.strip() for p in politikiFile]
        
        k = kljuci[0][0]
        i = 0
    
        while ((oznake[k][0:2] != "Sl") or (k in politiki) or (k in drzave.keys())) :
            i += 1
            k = kljuci[i][0]
    return k
        
        
        

def pridobiXML(pot):
        #Pridobi datoteke
    datoteke = [f for f in listdir(pot) if isfile(join(pot, f))]
    st = 0
    
    print("-----" + str(len(datoteke)) + " datotek pridobljenih-----")
    
    #Seznam lematiziranih clankov
    clanki_lem = []
    
    print("-----Razvrščanje besed v objekte-----")
    #Preberi datoteke v UTF-8
    
    for d in datoteke:
        if (st%100 == 0):
            print(".", end="")
        
        fileObj = codecs.open( pot + d, "r", "utf-8" )
        soup = BeautifulSoup(fileObj, 'xml')
        words = soup.find_all('w')
        datum = d.split("_")[1:]
        datum[-1] = datum[-1][0:4]
        clanki_lem.append([])
        
        #Pridobi besede in jih shrani v seznam
        for w in words:
            lb = LematiziranaBeseda(w['lemma'], w['msd'], w.get_text(), datum)
            clanki_lem[st].append(lb)
        
        st+=1
    
    return clanki_lem

def pridobiSamostalnikePridevnike(clanki_lem, kljuc, blizina=True):
    #Slovar pojavitev besed okrog ključa
    slovar = {}
    
    #Oznake najdenih besed
    oznake = {}
    
    print()
    print("--------------------Iskanje ključnih besed za ključ: " + kljuc + "---------------------------")
    for c in clanki_lem:
        dolz_c = len(c)
        idx = [i for i in range(0, dolz_c) if c[i].lemma.lower() == kljuc.lower()]
        #besede = []
        #print(".", end="")
        if ((len(idx) > 0) and blizina):
            for i in idx:
                zacetek = i-30
                konec = i+30
                if (zacetek < 0):
                    zacetek = 0
                if (konec > dolz_c):
                    konec = dolz_c
                
                for j in range(zacetek, konec):
                    if ((c[j].lemma != kljuc) and (((c[j].oznaka[0]) == "S") or (c[j].oznaka[0]) == "P")):
                        oznake[c[j].lemma] = c[j].oznaka
                        try:
                            slovar[c[j].lemma] += 1
                        except:
                            slovar[c[j].lemma] = 1
            
        elif ((len(idx)) > 0):
            for j in range(0, len(c)):
                if ((c[j].lemma != kljuc) and (((c[j].oznaka[0]) == "S") or (c[j].oznaka[0]) == "P")):
                    oznake[c[j].lemma.lower()] = c[j].oznaka
                    try:
                        slovar[c[j].lemma] += 1
                    except:
                        slovar[c[j].lemma] = 1
    #print()
    #print("Najdene so bile naslednje ključne besede s frekvenco:")
    najdene = sorted(slovar.items(), key=operator.itemgetter(1), reverse = True)
    
    #for n in najdene[:30]:
    #   print(n[0] + ": " + str(n[1]))
    
    return najdene, oznake
    

if __name__== "__main__":
    
    #Mapa
    pot = "./clanki_XML/"
    
    #Pridobimo lematizirane članke
    clanki_lem = pridobiXML(pot)
    
    filePolitiki = codecs.open("politiki2.txt", "r", "utf-8" )
    for p in filePolitiki:
        kljuc = p.strip()

        #Tip iskanja = True - pri iskanju poglej bližino ključa. False - poglej celoten članek
        blizina = True
            
        #poišči besede v okolici iskane
        najdene, oznake = pridobiSamostalnikePridevnike(clanki_lem, kljuc, blizina)
            
        print("Osebno ime:")
        ime = najdiIme(najdene, oznake)
        print("Ime in priimek iskane osebe: " + ime + " " + kljuc)
            
        print()
            
        print("Pripadajoča država:")
        d = najdiDrzavo(najdene)
        print(d[0][0] + " z verjetnostjo " + str(round(d[0][1]/(sum(n for _, n in d)) * 100, 2)) + "%")
            
        print()
            
        print("Besede, ki bi lahko nakazovale bias s frekvenco pojavitev:")
        b, s = najdiBias(najdene)
        print("Skupni bias: " + str(round(s, 2)))
        print(b[0:4])
                
        print()
                
        print("S politikom povezane ideologije s frekvenco pojavitev:")
        i = najdiIdeologijo(najdene)
        for ii in i[0:4]:
            print(ii[0] + " " + str(ii[1]))
#with open("clanki.txt", "rb") as fp:
#    clanki = pickle.load(fp)


