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

def getPts50(i):
    if i in pts50:
        return pts50[i]

def getPts60(i):
    if i in pts60:
        return pts60[i]

def getPts61(i):
    if i in pts61:
        return pts61[i]

def getPts91(i):
    if i in pts91:
        return pts91[i]

def getPts03(i):
    if i in pts03:
        return pts03[i]

def getPts10(i):
    if i in pts10:
        return pts10[i]

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
#        season = plain(a)
#        index = Season() 
#        index.year = season
#        index.save()
        href = a['href']
        year(opener, SITE + href)

def year(opener, url):
    soup = readurl(opener, 'YEAR', url)
    divname = soup.find('div', 'NavigCenter')
    #h1 = divname.find('h1')
    #season = int(plain(h1))
    table = soup.find('table', id='ctl00_CPH_Main_TBL_GPSaison')
#    if season >= 1950 and season <= 1959:
#        for i in range(1, len(pts50)+1):
#            point = Point()
#            point.season = Season.objects.get(year=season)
#            point.position = i
#            point.point = getPts50(i)
#            point.save()
#    if season == 1960:
#        for i in range(1, len(pts60)+1):
#            point = Point()
#            point.season = Season.objects.get(year=season)
#            point.position = i
#            point.point = getPts60(i)
#            point.save()
#    if season >= 1961 and season <= 1990:
#        for i in range(1, len(pts61)+1):
#            point = Point()
#            point.season = Season.objects.get(year=season)
#            point.position = i
#            point.point = getPts61(i)
#            point.save()
#    if season >= 1991 and season <= 2002:
#        for i in range(1, len(pts91)+1):
#            point = Point()
#            point.season = Season.objects.get(year=season)
#            point.position = i
#            point.point = getPts91(i)
#            point.save()    
#    if season >= 2003 and season <= 2009:
#        for i in range(1, len(pts03)+1):
#            point = Point()
#            point.season = Season.objects.get(year=season)
#            point.position = i
#            point.point = getPts03(i)
#            point.save()
#    if year == 2010:
#        for i in range(1, len(pts10)+1):
#            point = Point()
#            point.season = Season.objects.get(year=season)
#            point.position = i
#            point.point = getPts10(i)
#            point.save()
               
    for a in table.findAll('a'):
        href = a['href']
        grandprix(opener, SITE + href)
        

def grandprix(opener, url):
    soup = readurl(opener, 'GRANDPRIX', url)
    meteo = soup.find('img', id='ctl00_CPH_Main_IMG_Meteo')
    td = meteo.parent.nextSibling.nextSibling
    divname = soup.find('div', 'NavigCenter')
    h1 = divname.find('h1')
    title = plain(h1)
    parts = title.split(' ')
    index_p = parts[0]
    index_parts = index_p.split('.')
    index = index_parts[0]
    for a in h1.find('a'):
        name = plain(a)
        country = name
    if country == 'Indianapolis':
           country = 'USA'
    season = parts[2]
    slug = urlify(name) + '-' + season
    try:
        season_t = parts[3]
        slug = urlify(name) + '-' + season_t
    except:
        None
    
    track = plain(td.contents[1])
    date = cut(td.contents[0])
    dparts = date.split(' ')
    day = int(dparts[0])
    month = MONTH.index(dparts[1]) + 1
    year = int(dparts[2])

    info = cut(td.contents[3])
    kparts = info.split(' ')

    laps = int(kparts[0])
    len = kparts[3]
    lparts = len.split('.')
    temp_km = lparts[0] + lparts[1]
    km = int(temp_km)
    
    #print index
    #print name
    #print season
    #print track
    #print 'Date:', day, month, year 
    #print 'Laps:', laps
    #print 'Track len:', km

    #result = soup.find('a', id='ctl00_CPH_Main_HL_Classement')
    #best = soup.find('a', id='ctl00_CPH_Main_HL_MeilleurTour')
    #reshref = result['href']
    #besthref = best['href']
    #race(SITE + reshref)
    #bestlap(SITE + besthref)
    
    
#    test = TrackLen()
#    test.track = Track.objects.get(name=track)
#    fail = Track()
#    fail.tracklen = TrackLen.objects.get(track=test.track, length=km)
#    
#    grandprix = GrandPrix()
#    grandprix.index = index
#    try:
#        grandprix.season = Season.objects.get(year=season)
#    except:
#        grandprix.season = Season.objects.get(year=season_t)
#    grandprix.name = GPName.objects.get(name=name)
#    grandprix.slug = slug
#    #try:
#    grandprix.country = Country.objects.get(name=country)
#    #except:
#    #    grandprix.country = Country.objects.get(name='Unknown')
#    grandprix.tracklen = fail.tracklen
#    grandprix.save()

    # Going to Starting grid
    
    
    
    race_link = soup.find('a', id='ctl00_CPH_Main_HL_Classement')
    racehref = race_link['href']
    race(opener, SITE + racehref)
    

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
        #result[(first_name, family_name, team, engine)] = tyre
        result[(first_name, family_name)] = tyre, team, engine, num
    return result
    

        
#Race
def race(opener, url):
    soup = readurl(opener, 'race', url)
    entr = soup.find('a', id='ctl00_CPH_Main_Entete_HL_Engages')
    entrans_href = entr['href']
    tyre = None
    dsq = False
    dnf = False
    
    # открываем список заявленных пилотов
    result = entrans(opener, SITE + entrans_href)
    
    divname = soup.find('div', 'NavigCenter')
    h1 = divname.find('h1')
    slug = urlify(plain(h1)) + '-race'
    h1_parts = plain(h1).split(' ')
    gpname = ' '.join(h1_parts[0:-1]) # название гран-при
    season = int(h1_parts[-1]) # сезон
    re = h1.find('a')
    gp_link = re['href'] # нужно чтобы дёргать дату заезда
    
    tbody = soup.find('tbody')
    
    # дергаем данные победителя
    for tr in tbody.findAll('tr'):
        if plain(tr.contents[1]) == '1':
            try:
                winlaps = int(plain(tr.contents[6].contents[0]))
                results = plain(tr.contents[7].find('i'))
                try:
                    rparts = results.split(' ')
                    hours = Decimal(rparts[0].split('h')[0])
                    minutes = Decimal(rparts[1].split('m')[0])
                    etc = Decimal(rparts[2].split('s')[0])
                except:
                    hours = 0
                    minutes = Decimal(results.split("'")[0])
                    etc = Decimal(str(results.split("'")[1] + '.' + results.split("''")[1]))
                wintime = Decimal(hours * 3600 + minutes * 60 + etc)
                print 'Winner time:', wintime
                print 'Laps: ', winlaps
            except:
                print 'fail'
        else:
            pass
                
    test = GrandPrix()
    test.name = GPName.objects.get(en_name=gpname)
    test.season = Season.objects.get(year=season)
    
    r = Heat()
    r.grandprix = GrandPrix.objects.get(name=test.name, season=test.season)
    r.type = 'R'
    r.date = getdate(opener, SITE + gp_link)
    #wintime = Decimal(str(11197.800))
    if wintime < 3700:
        r.time = wintime
        r.half_points = True
        print 'KUKU'
    else:
        r.time = wintime
    r.laps = winlaps
    r.slug = slug
    r.save()


    
    # считаем количество финишировавших
    fcounter = 0
    for tr in tbody.findAll('tr'):
        try:
            position = int(plain(tr.contents[1]))
            fcounter += 1
        except:
            pass
    
    # считаем количество сошедших
    counter = 0
    for tr in tbody.findAll('tr'):
        position = plain(tr.contents[1])
        if position == 'ab':
            counter += 1
            
    # считаем количество dsq
    dcounter = 0
    for tr in tbody.findAll('tr'):
        position = plain(tr.contents[1])
        laps = plain(tr.contents[6])
        if laps == '' or laps == 'tf':
            laps is None
            laps_gap = None
        else:
            laps_gap = int(winlaps) - int(laps)
        if position == 'dsq' and laps_gap <= (winlaps/10 + 1):
            dcounter += 1

    #tr_count = fcounter + counter 
            
            
    for tr in tbody.findAll('tr'):
        position = plain(tr.contents[1])
        laps = plain(tr.contents[6])
        if laps == '' or laps == 'tf':
            laps is None
            laps_gap = None
        else:
            laps_gap = int(winlaps) - int(laps)
        fail = ''
        if position == '' or position == 'f' or position == 'nq' or position == 'npq' or position == 'exc' or position == 'np':
            pass
        else:
            # определяем позицию пилота
            if position == 'dsq':
                #pos = 16
                dsq = True
                dnf = False
            else:
                dsq = False
            if position == 'ab':
                dsq = False
                dnf = True
            else:
                dnf = False
            try:
                pos = Decimal(position)
            except:
                if position == '&amp;':
                    pos = pos
                else:
                    pos += 1
            #num = plain(tr.contents[2])
            racer_a = tr.contents[3].find('a')
            racer_href = racer_a['href']
            racer = getRacer(racer_href)
            parts = racer.split(' ')
            first_name = urlify(parts[0]).capitalize()
            family_name = get_last_name(parts)
            team = plain(tr.contents[4])
            engine = plain(tr.contents[5])
            if engine == 'Pratt &amp; Whitney':
                engine = 'Pratt & Whitney'
            elif engine == 'K&#252;chen':
                engine = 'Kuchen'
            try:
                #tyre = result[(first_name, family_name, team, engine)]
                tyre, team, engine, num = result[(first_name, family_name)]
            except IndexError:
                tyre = None

            
            # проверяем время или сход
            try:
                time = plain(tr.contents[7].find('i'))
                try:
                    tparts = time.split(' ')
                    hours = Decimal(tparts[0].split('h')[0])
                    minutes = Decimal(tparts[1].split('m')[0])
                    etc = Decimal(tparts[2].split('s')[0])
                except:
                    hours = 0
                    minutes = Decimal(time.split("'")[0])
                    etc = Decimal(str(time.split("'")[1] + '.' + time.split("''")[1]))
                result_time = str(hours * 3600 + minutes * 60 + etc)
                time_gap = abs(Decimal(wintime) - Decimal(result_time))
                if tr.contents[7].find('br'):
                    fail = plain(tr.contents[7].find('br').previousSibling)
            except:
                results = plain(tr.contents[7])
                if results == '':
                    time_gap = None
                    fail = None
                else:
                    fail = results
                    time_gap = None

            
            rac = Racer()
            rac.en_first_name = first_name
            rac.en_family_name = family_name

            ret = Retire()
            ret.en_reason = fail
            
            race = Result()
            race.heat = Heat.objects.get(grandprix=r.grandprix, type=r.type)
            race.position = pos
            race.num = num
            race.racer = Racer.objects.get(en_first_name=rac.en_first_name, en_family_name=rac.en_family_name)
            race.team = Team.objects.get(name=team)
            race.engine = Engine.objects.get(name=engine)
            race.tyre = Tyre.objects.get(name=tyre)
            race.delta = time_gap
            race.laps = laps_gap
            try:
                race.retire = Retire.objects.get(en_reason=ret.en_reason)
            except Retire.DoesNotExist:
                race.retire = None
            race.dsq = dsq
            race.save()
            
            print pos, num, first_name, family_name, team, engine, tyre, laps, laps_gap, time_gap, fail, dnf, dsq
            
            
        
def main():
    opener = urllib2.build_opener()



    #index(opener, SITE + '/en/saisons.aspx')
    #year(opener, 'http://statsf1.com/en/1968.aspx')
    #race(opener, 'http://statsf1.com/en/1990/monaco/classement.aspx')
    race(opener, 'http://statsf1.com/en/2011/chine/classement.aspx')
    
if __name__ == '__main__':
    main()
else:
    from f1info.models import *
