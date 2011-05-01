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

SITE = 'http://www.formula1.com'
MONTH = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', ]

tyres = {
         'Ferrari': 'Bridgestone',
         'Sauber': 'Bridgestone',
         'BAR': 'Bridgestone',
         'Jordan': 'Bridgestone',
         'Minardi': 'Bridgestone',
         'McLaren': 'Michelin',
         'Williams': 'Michelin',
         'Renault': 'Michelin',
         'Toyota': 'Michelin',
         'Jaguar': 'Michelin',
}

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
    fp(opener, SITE + gridhref)    
    
      
#Free practice
def fp(opener, url):
    soup = readurl(opener, 'fp', url)

    links = soup.find('div', id='tertiaryNav') #List of seasons
    season = plain(links.contents[1].contents[1]) #Current season
    gp = plain(links.contents[1].contents[5]) #Current Grand Prix
    type = plain(links.contents[1].contents[9]) #Heat type
    
    if type == 'FRIDAY PRACTICE':
        print 'FP1'
    elif type == 'THURSDAY PRACTICE':
        print 'FP1'
    elif type == 'SATURDAY PRACTICE 1':
        print 'FP2'
    elif type == 'SATURDAY PRACTICE 2':
        print 'FP3'
    
    
    results = soup.find('table', 'raceResults')
    
    #Searching for the First place
    for tr in results.findAll('tr')[1:2]:
        pos = plain(tr.contents[1]) #Position
        num = plain(tr.contents[3]) #Car number
        racer = plain(tr.contents[5]) #Racer
        parts = racer.split(' ')
        first_name = urlify(parts[0]).capitalize()
        family_name = get_last_name(parts)
        
        team_engine = plain(tr.contents[7]) #Team-Engine 
        try:
            dash = team_engine.split('-')
            team = dash[0] #Team
            engine = dash[1] #Engine
        except:
            team = plain(tr.contents[7])
            engine = plain(tr.contents[7])
        
        tyre = tyres[team]
        
        win_time = plain(tr.contents[9])
        wparts = win_time.split(':')
        mins = int(wparts[0])
        seconds = int((wparts[1].split('.'))[0])
        etc = Decimal((wparts[1].split('.'))[1]) / 1000
        wtime = Decimal(60*mins + seconds + etc) #Winner's time
        
        print pos, num, first_name, family_name, team, engine, tyre, wtime
        
    #Searching for the other places
    for tr in results.findAll('tr')[2:]:
        pos = plain(tr.contents[1]) #Position
        num = plain(tr.contents[3]) #Car number
        racer = plain(tr.contents[5]) #Racer
        parts = racer.split(' ')
        first_name = urlify(parts[0]).capitalize()
        family_name = get_last_name(parts)
        
        team_engine = plain(tr.contents[7]) #Team-Engine 
        try:
            dash = team_engine.split('-')
            team = dash[0] #Team
            engine = dash[1] #Engine
        except:
            team = plain(tr.contents[7])
            engine = plain(tr.contents[7])
        
        tyre = tyres[team]
        
        dl = plain(tr.contents[11])
        if dl == '':
            delta = None
        else:
            dparts = dl.split('.')
            seconds = int(dparts[0])
            etc = Decimal(dparts[1]) / 1000
            delta = Decimal(seconds + etc) #Delta
        
        print pos, num, first_name, family_name, team, engine, tyre, delta
    


def main():
    opener = urllib2.build_opener()
    #year(opener, 'http://statsf1.com/en/2010.aspx')
    fp(opener, 'http://www.formula1.com/results/season/2003/22/172/')

if __name__ == '__main__':
    main()
else:
    from f1info.models import *
