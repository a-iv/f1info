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
    grid = soup.find('a', id='ctl00_CPH_Main_HL_Qualification')
    gridhref = grid['href']
    qual(opener, SITE + gridhref)
    

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
        result[(first_name, family_name, team, engine)] = (num, tyre)
    return result
        
#Starting grid
def qual(opener, url):
    soup = readurl(opener, 'qual', url)
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
    slug = urlify(plain(h1)) + '-qual'
    h1_parts = plain(h1).split(' ')
    gpname = ' '.join(h1_parts[0:-1]) # название гран-при
    season = int(h1_parts[-1]) # сезон
    re = h1.find('a')
    gp_link = re['href'] # нужно чтобы дёргать дату заезда
    
    tbody = soup.find('tbody')
    if tbody is None:
        gp = GrandPrix()
        gp.name = GPName.objects.get(name=gpname)
        gp.season = Season.objects.get(year=season)
        
        q = Heat()
        q.grandprix = GrandPrix.objects.get(name=gp.name, season=gp.season)
        q.type = 'Q'
        q.date = getdate(opener, SITE + gp_link)
        q.time = wtime
        q.laps = 0
        q.slug = slug
        q.save()
        pass
    else:
        for tr in tbody.findAll('tr')[0:1]:
            pos = plain(tr.contents[1])
            if pos =='':
                pass
            else:
                racer_a = tr.contents[2].find('a')
                racer_href = racer_a['href']
                racer = getRacer(racer_href)
                parts = racer.split(' ')
                first_name = urlify(parts[0]).capitalize()
                family_name = get_last_name(parts)
                team = plain(tr.contents[3])
                engine = plain(tr.contents[4])
                if engine == 'Pratt &amp; Whitney':
                    engine = 'Pratt & Whitney'
                elif engine == 'K&#252;chen':
                    engine = 'Kuchen'
                time = plain(tr.contents[5])
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
                
                try:
                    num, tyre = result[(first_name, family_name, team, engine)]
                except IndexError:
                    num, tyre = 0, None
                    
                print pos, num, first_name, family_name, team, engine, wtime
            
                gp = GrandPrix()
                gp.name = GPName.objects.get(name=gpname)
                gp.season = Season.objects.get(year=season)
                
                q = Heat()
                q.grandprix = GrandPrix.objects.get(name=gp.name, season=gp.season)
                q.type = 'Q'
                q.date = getdate(opener, SITE + gp_link)
                q.time = wtime
                q.laps = 0
                q.slug = slug
                q.save()
                
                r = Racer()
                r.first_name = first_name
                r.family_name = family_name
                
                qual = Result()
                qual.heat = Heat.objects.get(grandprix=q.grandprix)
                qual.position = 1
                qual.num = num
                qual.racer = Racer.objects.get(first_name=r.first_name, family_name=r.family_name)
                qual.team = Team.objects.get(name=team)
                qual.engine = Engine.objects.get(name=engine)
                qual.tyre = Tyre.objects.get(name=tyre)
                qual.delta = 0
                qual.save()
        
        for tr in tbody.findAll('tr')[1:]:
            pos = plain(tr.contents[1])
            if pos =='':
                pass
            else:
                racer_a = tr.contents[2].find('a')
                racer_href = racer_a['href']
                racer = getRacer(racer_href)
                parts = racer.split(' ')
                first_name = urlify(parts[0]).capitalize()
                family_name = get_last_name(parts)
                team = plain(tr.contents[3])
                engine = plain(tr.contents[4])
                if engine == 'Pratt &amp; Whitney':
                    engine = 'Pratt & Whitney'
                elif engine == 'K&#252;chen':
                    engine = 'Kuchen'
                try:
                    delta = Decimal(plain(tr.contents[6]))
                except:
                    delta = None
                
                try:
                    num, tyre = result[(first_name, family_name, team, engine)]
                except IndexError:
                    num, tyre = 0, None
      
                r = Racer()
                r.first_name = first_name
                r.family_name = family_name
                
                qual = Result()
                qual.heat = Heat.objects.get(grandprix=q.grandprix)
                qual.position = pos
                qual.num = num
                qual.racer = Racer.objects.get(first_name=r.first_name, family_name=r.family_name)
                qual.team = Team.objects.get(name=team)
                qual.engine = Engine.objects.get(name=engine)
                qual.tyre = Tyre.objects.get(name=tyre)
                qual.delta = delta
                qual.save()
            
                print pos, num, first_name, family_name, team, engine, delta


def main():
    realm = 'Squid proxy-caching web server'
    host = 'proxy.hq.redsolution.ru:3128'
    user = 'alexey.kuligin'
    password = ''

    proxy_handler = urllib2.ProxyHandler({'http': 'http://%s/' % host})
    proxy_auth_handler = urllib2.ProxyBasicAuthHandler()
    proxy_auth_handler.add_password(realm, host, user, password)
    opener = urllib2.build_opener() #proxy_handler, proxy_auth_handler)

    year(opener, 'http://statsf1.com/en/2010.aspx')
    #entrans(opener, 'http://statsf1.com/en/1952/suisse/engages.aspx')
    #qual(opener, 'http://statsf1.com/en/1978/canada/qualification.aspx')

if __name__ == '__main__':
    main()
else:
    from f1info.models import *
