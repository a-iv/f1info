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
MONTH = ['january', 'february', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'december', ]

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
    ul_years = soup.find('div', id='tertiaryNav')
    ul_gp = ul_years.contents[1].contents[7]
    for a in ul_gp.findAll('a')[17:]:
        href = a['href']
        grandprix(opener, SITE + href)
        
def grandprix(opener, url):
    soup = readurl(opener, 'GRANDPRIX', url)
    ul_years = soup.find('div', id='tertiaryNav')
    ul_gp = ul_years.contents[1].contents[11]
    for a in ul_gp.findAll('a')[:3]:
        href = a['href']
        fp(opener, SITE + href)    
    
      
#Free practice
def fp(opener, url):
    soup = readurl(opener, 'fp', url)

    links = soup.find('div', id='tertiaryNav') #List of seasons
    season = plain(links.contents[1].contents[1]) #Current season
    try:    
        gpn = plain(links.contents[1].contents[5]).split(' ') #Current Grand Prix
        gpname = gpn[0].capitalize() + ' ' + gpn[1].capitalize()
    except:
        gpname = plain(links.contents[1].contents[5]).capitalize()
    type = plain(links.contents[1].contents[9]) #Heat type
    print type

    types = {
        'PRACTICE 1': '1',
        'PRACTICE 2': '2',
        'PRACTICE 3': '3',
    }
    slug = urlify(gpname) + '-' + str(season) + '-' + 'fp' + urlify(types[type])
    print gpname
    print slug

    heading = soup.find('div', 'raceResultsHeading')
    gpdate = plain(heading.find('span'))
    gparts = gpdate.split(' ')
    day = int(gparts[0])
    try:    
        month = MONTH.index(gparts[3]) + 1
    except:
        month = MONTH.index(gparts[1]) + 1


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
            if team == 'BMW Sauber':
                engine = 'BMW'
            elif team == 'Mercedes GP':
                engine = 'Mercedes'
            else:
                engine = plain(tr.contents[7])
        
        tyre = 'Pirelli'
        
        win_time = plain(tr.contents[9])
        wparts = win_time.split(':')
        mins = int(wparts[0])
        seconds = int((wparts[1].split('.'))[0])
        etc = Decimal((wparts[1].split('.'))[1]) / 1000
        wtime = Decimal(60*mins + seconds + etc) #Winner's time
        
        gp = GrandPrix()
        if gpname == 'Great Britain':
            gp.name = GPName.objects.get(en_name='Britain')
        elif gpname == 'United States':
            gp.name = GPName.objects.get(en_name='USA')
        elif gpname == 'Korea':
            gp.name = GPName.objects.get(en_name='South Korea')
        else:
            gp.name = GPName.objects.get(en_name=gpname)
        gp.season = Season.objects.get(year=season)
        
        print gp.name, gp.season
        
        q = Heat()
        q.grandprix = GrandPrix.objects.get(name=gp.name, season=gp.season)
        q.type = types[type]
        if types[type] == '1' or types[type] == '2':
            q.date = datetime.datetime(int(season), int(month), day, 0, 0)
        elif types[type] == '3' or types[type] == '4':
            if gpname == 'Monaco':
                q.date = datetime.datetime(int(season), int(month), day+2, 0, 0)
            else:
                q.date = datetime.datetime(int(season), int(month), day+1, 0, 0)
        print q.date
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
        if team == 'RBR':
            qual.team = Team.objects.get(name='Red Bull')
        elif team == 'STR':
            qual.team = Team.objects.get(name='Toro Rosso')
        elif team == 'Mercedes GP':
            qual.team = Team.objects.get(name='Mercedes')
        else:
            qual.team = Team.objects.get(name=team)
        qual.engine = Engine.objects.get(name=engine)
        qual.tyre = Tyre.objects.get(name=tyre)
        qual.delta = 0
        qual.save()

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
            if team == 'BMW Sauber':
                engine = 'BMW'
            elif team == 'Mercedes GP':
                engine = 'Mercedes'
            else:
                engine = plain(tr.contents[7])
        
        tyre = 'Pirelli'
        
        dl = plain(tr.contents[11])
        if dl == '':
            delta = None
        else:
            dparts = dl.split('.')
            seconds = int(dparts[0])
            etc = Decimal(dparts[1]) / 1000
            delta = Decimal(seconds + etc) #Delta
        
        r = Racer()
        r.en_first_name = first_name
        r.en_family_name = family_name
        
        qual = Result()
        qual.heat = Heat.objects.get(grandprix=q.grandprix, type=q.type)
        qual.position = pos
        qual.num = num
        qual.racer = Racer.objects.get(en_first_name=r.en_first_name, en_family_name=r.en_family_name)
        if team == 'RBR':
            qual.team = Team.objects.get(name='Red Bull')
        elif team == 'STR':
            qual.team = Team.objects.get(name='Toro Rosso')
        elif team == 'Mercedes GP':
            qual.team = Team.objects.get(name='Mercedes')
        else:
            qual.team = Team.objects.get(name=team)
        qual.engine = Engine.objects.get(name=engine)
        qual.tyre = Tyre.objects.get(name=tyre)
        qual.delta = delta
        qual.save()
        
        print pos, num, first_name, family_name, team, engine, tyre, delta
    


def main():
    opener = urllib2.build_opener()
    fp(opener, 'http://www.formula1.com/results/season/2011/857/6857/')
    fp(opener, 'http://www.formula1.com/results/season/2011/857/6858/')
    fp(opener, 'http://www.formula1.com/results/season/2011/857/6860/')

if __name__ == '__main__':
    main()
else:
    from f1info.models import *
