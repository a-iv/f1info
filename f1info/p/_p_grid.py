# -*- coding: utf-8 -*-

from beautifulsoup import BeautifulSoup, Tag
import re
import os
import urllib2
import datetime
from urltoracer import urls
from ractoracer import racs
from syspts import *
from decimal import *
from urlify import *

SITE = 'http://statsf1.com'
MONTH = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', ]

def getRacer(url):
    if url in urls:
        return urls[url]

def getRac(short):
    if short in racs:
        return racs[short]

def readurl(opener, name, url):
    print '%s: %s' % (name, url)
    opened = opener.open(url)
    data = opened.read()
    open('debug.html', 'w').write(data)
    return BeautifulSoup(data)
  
def cut(value):
    return (re.sub(r'(&nbsp;|\s)+', ' ', unicode(value))).strip()

def plain(soup):
    result = u''
    for content in soup:
        if isinstance(content, Tag):
            result += plain(content)
        else:
            result += content
    return cut(result)

def get_last_name(list):
    f = ''
    for i in list[1:-1]:
        f = f + urlify(i).capitalize() + ' '
    f = f + urlify(list[-1]).capitalize()
    return f


def index(opener, url):
    soup = readurl(opener, 'INDEX', url)
    table = soup.find('table', id='ctl00_CPH_Main_TBL_Annee')
    for a in table.findAll('a'):
        href = a['href']
        year(opener, SITE + href)

def year(opener, url):
    soup = readurl(opener, 'YEAR', url)
    divname = soup.find('div', 'NavigCenter')
    table = soup.find('table', id='ctl00_CPH_Main_TBL_GPSaison')
    for a in table.findAll('a'):
        href = a['href']
        grandprix(opener, SITE + href)
        

def grandprix(opener, url):
    soup = readurl(opener, 'GRANDPRIX', url)
    link = soup.find('a', id='ctl00_CPH_Main_HL_Grille')
    linkhref = link['href']
    grid(opener, SITE + linkhref)
    

def getdate(opener, url):
    soup = readurl(opener, 'GRANDPRIX', url)
    meteo = soup.find('img', id='ctl00_CPH_Main_IMG_Meteo')
    td = meteo.parent.nextSibling.nextSibling
    date = cut(td.contents[0])
    dparts = date.split(' ')
    day = int(dparts[0])
    month = MONTH.index(dparts[1]) + 1
    year = int(dparts[2])
    gpdate = datetime.datetime(int(year), int(month), int(day))
    return gpdate
    
def entrans(opener, url):
    soup = readurl(opener, 'entrans', url)
    tbody = soup.find('tbody')
    result = {}
    for tr in tbody.findAll('tr'):
        num = plain(tr.contents[1])
        rac = tr.contents[2]
        racer_a = rac.find('a')
        href = racer_a['href']
        racer = getRacer(href)
        #print racer
        parts = racer.split(' ')
        first_name = urlify(parts[0]).capitalize()
        family_name = get_last_name(parts)
        #print first_name, family_name
        team = plain(tr.contents[4])
        engine = plain(tr.contents[6])
        if engine == 'Pratt &amp; Whitney':
            engine = 'Pratt & Whitney'
        elif engine == 'K&#252;chen':
            engine = 'Kuchen'
        tyre = plain(tr.contents[8])
        if tyre == '?':
            tyre = 'Unknown'
        result[(first_name, family_name, team)] = (num, tyre, engine)
    return result
        
#Starting grid
def grid(opener, url):
    soup = readurl(opener, 'grid', url)
    entr = soup.find('a', id='ctl00_CPH_Main_Entete_HL_Engages')
    entrans_href = entr['href']

    wtime = 0
    slug = None
    num = 0
    tyre = None
    
    # открываем список заявленных пилотов
    result = entrans(opener, SITE + entrans_href)
    
    divname = soup.find('div', 'NavigCenter')
    h1 = divname.find('h1')
    slug = urlify(plain(h1)) + '-grid'
    h1_parts = plain(h1).split(' ')
    gpname = ' '.join(h1_parts[0:-1]) # название гран-при
    season = int(h1_parts[-1]) # сезон
    re = h1.find('a')
    gp_link = re['href'] # нужно чтобы дёргать дату заезда
    
    table = soup.find('table', id='ctl00_CPH_Main_TBL_Grille')
    if table is None:
        print 'None'
    else:  

        for td in table.findAll('td', 'Grille'): 
            if td.find('strong'):
                if td.find('div', 'NP'):
                    pole = td.find('div', 'NP')
                else:
                    pole = td.find('div')

                pos = 1
                racer = getRacer(pole.contents[2]['href'])
                parts = racer.split(' ')
                first_name = urlify(parts[0]).capitalize()
                family_name = get_last_name(parts)
                team = plain(pole.contents[4])
                try:
                    num, tyre, engine = result[(first_name, family_name, team,)]
                except IndexError:
                    num, tyre, engine = 0, None
                time = plain(pole.contents[6])
                tparts = time.split("'")
                if len(tparts) > 1:
                    mins = int(tparts[0])
                    seconds = int(tparts[1])
                    try:
                        if len(tparts[3]) == 1:
                            etc = Decimal(tparts[3]) / 10
                        elif len(tparts[3]) == 2:
                            etc = Decimal(tparts[3]) / 100
                        elif len(tparts[3]) == 3:
                            etc = Decimal(tparts[3]) / 1000
                    except:
                        etc = 0
                    wtime = Decimal(60*mins + seconds + etc)
                else:
                    time = plain(pole.contents[8])
                    tparts = time.split("'")
                    mins = int(tparts[0])
                    seconds = int(tparts[1])
                    try:
                        if len(tparts[3]) == 1:
                            etc = Decimal(tparts[3]) / 10
                        elif len(tparts[3]) == 2:
                            etc = Decimal(tparts[3]) / 100
                        elif len(tparts[3]) == 3:
                            etc = Decimal(tparts[3]) / 1000
                    except:
                        etc = 0
                    wtime = Decimal(60*mins + seconds + etc)

                gp = GrandPrix()
                gp.name = GPName.objects.get(en_name=gpname)
                gp.season = Season.objects.get(year=season)
                
                q = Heat()
                q.grandprix = GrandPrix.objects.get(name=gp.name, season=gp.season)
                q.type = 'G'
                q.date = getdate(opener, SITE + gp_link)
                q.time = wtime
                q.laps = 0
                q.slug = slug
                q.save()


                r = Racer()
                r.en_first_name = first_name
                r.en_family_name = family_name

                qual = Result()
                qual.heat = Heat.objects.get(grandprix=q.grandprix, type=q.type)
                qual.position = 1
                qual.num = num
                qual.racer = Racer.objects.get(en_first_name=r.en_first_name, en_family_name=r.en_family_name)
                qual.team = Team.objects.get(name=team)
                qual.engine = Engine.objects.get(name=engine)
                qual.tyre = Tyre.objects.get(name=tyre)
                qual.delta = 0
                qual.save() 

                print pos, first_name, family_name, team, engine, wtime
            

        
        for td in table.findAll('td', 'Grille'):
            if td.find('strong'):
                pass
                
            else:
                if td.find('div', 'NP'):
                    cell = td.find('div', 'NP')
                else:
                    cell = td.find('div')
                if plain(td) == '':
                    pass
                else:
                    pos = plain(cell.contents[0].split('.')[0])
                    racer = getRacer(cell.contents[1]['href'])
                    parts = racer.split(' ')
                    first_name = urlify(parts[0]).capitalize()
                    family_name = get_last_name(parts)
                    team = plain(cell.contents[3])
                    try:
                        num, tyre, engine = result[(first_name, family_name, team,)]
                    except IndexError:
                        num, tyre, engine = 0, None
                    
                    time = plain(cell.find('i'))
                    if time:
                        tparts = time.split("'")
                        mins = int(tparts[0])
                        seconds = int(tparts[1])
                        try:
                            if len(tparts[3]) == 1:
                                etc = Decimal(tparts[3]) / 10
                            elif len(tparts[3]) == 2:
                                etc = Decimal(tparts[3]) / 100
                            elif len(tparts[3]) == 3:
                                etc = Decimal(tparts[3]) / 1000
                        except:
                            etc = 0
                        gtime = Decimal(60*mins + seconds + etc)
                        delta = Decimal(gtime, 3) - Decimal(wtime, 3)
                    else:
                        gtime = None
                        delta = None
                    
                    
                    r = Racer()
                    r.en_first_name = first_name
                    r.en_family_name = family_name
                                       
                    qual = Result()
                    qual.heat = Heat.objects.get(grandprix=q.grandprix, type=q.type)
                    qual.position = pos
                    qual.num = num
                    qual.racer = Racer.objects.get(en_first_name=r.en_first_name, en_family_name=r.en_family_name)
                    qual.team = Team.objects.get(name=team)
                    qual.engine = Engine.objects.get(name=engine)
                    qual.tyre = Tyre.objects.get(name=tyre)
                    qual.delta = delta
                    qual.save() 
                    
                    print pos, first_name, family_name, team, engine, gtime, delta
        



def main():
    opener = urllib2.build_opener()
    #entrans(opener, 'http://statsf1.com/en/1952/suisse/engages.aspx')

    grid(opener, 'http://statsf1.com/en/2011/australie/grille.aspx')
    grid(opener, 'http://statsf1.com/en/2011/malaisie/grille.aspx')
    grid(opener, 'http://statsf1.com/en/2011/chine/grille.aspx')
    grid(opener, 'http://statsf1.com/en/2011/turquie/grille.aspx')
    grid(opener, 'http://statsf1.com/en/2011/espagne/grille.aspx')
    grid(opener, 'http://statsf1.com/en/2011/monaco/grille.aspx')
    grid(opener, 'http://statsf1.com/en/2011/canada/grille.aspx')
    grid(opener, 'http://statsf1.com/en/2011/europe/grille.aspx')

if __name__ == '__main__':
    main()
else:
    from f1info.models import *
