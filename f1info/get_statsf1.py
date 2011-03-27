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
    
    
    
    grid = soup.find('a', id='ctl00_CPH_Main_HL_Grille')
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
    
    
    
def gplist(opener, url):
    soup = readurl(opener, 'GPLIST', url)
    table = soup.find('table', id='ctl00_CPH_Main_GV_GrandPrix')
    for tr in table.findAll('tr'):
        link = tr.contents[1]       
        for a in link.findAll('a'):      
            link = plain(a)
            gplist = GPName()
            gplist.name = link
            gplist.en_name = link
            gplist.save()


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
        print first_name, family_name
        team = plain(tr.contents[4])
        engine = plain(tr.contents[6])
        if engine == 'Pratt &amp; Whitney':
            engine = 'Pratt & Whitney'
        elif engine == 'K&#252;chen':
            engine = 'Kuchen'
        tyre = plain(tr.contents[8])
        if tyre == '?':
            tyre = 'Unknown'
        #print racer
        result[(first_name, family_name, team, engine)] = (num, tyre)
        #result[(first_name, family_name, team, engine)] = tyre
    return result
        
#Race
def race(opener, url):
    soup = readurl(opener, 'race', url)
    entr = soup.find('a', id='ctl00_CPH_Main_Entete_HL_Engages')
    entrans_href = entr['href']
    tyre = None
    result = entrans(opener, SITE + entrans_href)
    divname = soup.find('div', 'NavigCenter')
    h1 = divname.find('h1')
    for a in h1.find('a'):
        slug_t = plain(a)
        slpart = slug_t.split(' ')
        slug = (plain('-'.join(slpart[0:])) + '-r').lower() 
        gpname = plain(' '.join(slpart[0:-1]))
        season = int(slpart[-1])
        print gpname, season
    re = h1.find('a')
    gp_link = re['href']
    tbody = soup.find('tbody')
    for tr in tbody.findAll('tr')[0:1]:
        winlaps = int(plain(tr.contents[6].contents[0]))
        results = plain(tr.contents[7])
        rparts = results.split(' ')
        tmp_hours = rparts[0]
        hparts = tmp_hours.split('h')
        hours = Decimal(hparts[0])
        tmp_minutes = rparts[1]
        mparts = tmp_minutes.split('m')
        minutes = Decimal(mparts[0])
        tmp_etc = rparts[2]
        sparts = tmp_etc.split('s')
        etc = Decimal(sparts[0])
        wintime = str(hours * 3600 + minutes * 60 + etc)
    print 'Winner time:', wintime
    print 'Laps: ', winlaps
    
    test = GrandPrix()
    test.name = GPName.objects.get(name=gpname)
    test.season = Season.objects.get(year=season)
    
    r = Heat()
    r.grandprix = GrandPrix.objects.get(name=test.name, season=test.season)
    r.type = 'R'
    r.date = getdate(opener, SITE + gp_link)
    r.time = wintime
    r.laps = winlaps
    r.slug = slug
    r.save()

               
    for tr in tbody.findAll('tr'):
        fail = ''
        lap_gap = 0
        position = str(plain(tr.contents[1].contents[0]))
        try:
            if position == '':
                continue
            pos = Decimal(position)
        except:
            pos += 1
        num = tr.contents[2].contents[0]
        racer_l = tr.contents[3]
        racer_a = racer_l.find('a')
        href = racer_a['href']
        racer = getRacer(href)
        parts = racer.split(' ')
        en_parts = []
        for i in range(0, len(parts) - 1):
            first_parts = plain(parts[i]).capitalize() + ' '            
            en_parts.append(first_parts)
        first_name = plain(en_parts)
        family_name = plain(parts[-1]).capitalize()
        team = plain(tr.contents[4])
        engine = plain(tr.contents[5])
        lap = plain(tr.contents[6].contents[0])
        if lap == '' or lap == 'tf':
            lap is None
        ### BETA ###
        if position == 'ab' or position == 'np':
            lap_gap = winlaps - int(lap)
        else:
            lap_gap = winlaps - int(lap)
        ### End ###
        
        try:
            results = tr.contents[7]
            resu = plain(results)
            i = results.find('i')
            ii = plain(i)
            rparts = ii.split(' ')
            tmp_hours = rparts[0]
            hparts = tmp_hours.split('h')
            hours = Decimal(hparts[0])
            tmp_minutes = rparts[1]
            mparts = tmp_minutes.split('m')
            minutes = Decimal(mparts[0])
            tmp_etc = rparts[2]
            sparts = tmp_etc.split('s')
            etc = Decimal(sparts[0])
            time = str(hours * 3600 + minutes * 60 + etc)
            res = abs(Decimal(wintime) - Decimal(time))
            lap_gap = 0
            fail = ''
        except:
            results = plain(tr.contents[7])
            if resu == '':
                res = None
                fail = ''
            else:
                res = None
                fail = results
        
        tyre = result[(first_name, family_name, team, engine)]
        
        rac = Racer()
        rac.first_name = first_name
        rac.family_name = family_name
        
        race = Result()
        race.heat = Heat.objects.get(grandprix=r.grandprix, type=r.type)
        race.position = pos
        race.num = num
        race.racer = Racer.objects.get(first_name=rac.first_name, family_name=rac.family_name)
        race.team = Team.objects.get(name=team)
        race.engine = Engine.objects.get(name=engine)
        race.tyre = Tyre.objects.get(name=tyre)
        race.delta = res
        race.laps = lap_gap
        race.fail = fail
        race.save()
        
        print pos, num, first_name, family_name, team, engine, tyre, lap, lap_gap, res


#Starting grid
def qual(opener, url):
    soup = readurl(opener, 'qual', url)
    entr = soup.find('a', id='ctl00_CPH_Main_Entete_HL_Engages')
    entrans_href = entr['href']
    table = soup.find('table', id='ctl00_CPH_Main_TBL_Grille')
    wtime = 0
    slug = 0
    num = 0
    tyre = None
    result = entrans(opener, SITE + entrans_href)
    divname = soup.find('div', 'NavigCenter')
    h1 = divname.find('h1')
    for a in h1.find('a'):
        slug_t = plain(a)
        slpart = slug_t.split(' ')
        slug = (plain('-'.join(slpart[0:])) + '-q').lower() 
        gpname = plain(' '.join(slpart[0:-1]))
        season = int(slpart[-1])
        print gpname, season
    re = h1.find('a')
    gp_link = re['href']
    
    for p in table.findAll('div', 'GrillePos'):
        temp = plain(p)
        parts = temp.split('.')
        pos = parts[0]
        if p.find('strong'):
            if len(p) > 8: 
                href = p.contents[2]['href']
                racer = getRacer(href)
                parts = racer.split(' ')
                first_name = urlify(parts[0]).capitalize()
                family_name = get_last_name(parts)
                team = plain(p.contents[4])
                engine = plain(p.contents[6])
                time = plain(p.contents[8])
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
            #    wtime = str(60*mins + seconds + etc/1000)
                
            else:
                href = p.contents[2]['href']
                racer = getRacer(href)
                parts = racer.split(' ')
                first_name = urlify(parts[0]).capitalize()
                family_name = get_last_name(parts)
                team = plain(p.contents[4])
                engine = team
                time = plain(p.contents[6])
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
            wtime = str(60 * mins + seconds + etc)
        else:
            continue
        
        try:
            num, tyre = result[(first_name, family_name, team, engine)]
        except IndexError:
            num, tyre = 0, None
        print pos, num, first_name, family_name, team, engine, tyre, wtime
        
#        test = GrandPrix()
#        test.name = GPName.objects.get(name=gpname)
#        test.season = Season.objects.get(year=season)
#        
#        q = Heat()
#        q.grandprix = GrandPrix.objects.get(name=test.name, season=test.season)
#        q.type = 'Q'
#        q.date = getdate(opener, SITE + gp_link)
#        q.time = wtime
#        q.laps = 0
#        q.slug = slug
#        q.save()
#        
#        r = Racer()
#        r.first_name = first_name
#        r.family_name = family_name
#        
#        qual = Result()
#        qual.heat = Heat.objects.get(grandprix=q.grandprix)
#        qual.position = 1
#        qual.num = num
#        qual.racer = Racer.objects.get(first_name=r.first_name, family_name=r.family_name)
#        qual.team = Team.objects.get(name=team)
#        qual.engine = Engine.objects.get(name=engine)
#        qual.tyre = Tyre.objects.get(name=tyre)
#        qual.delta = 0
#        qual.save()
            
    for p in table.findAll('div', 'GrillePos'):
        temp = plain(p)
        parts = temp.split('.')
        pos = parts[0]
        if p.find('strong'):
            continue

        if p.find:
            href = p.contents[1]['href']
            racer = getRacer(href)
            parts = racer.split(' ')
            first_name = urlify(parts[0]).capitalize()
            family_name = get_last_name(parts)
            team = plain(p.contents[3])
            if len(p) < 8: 
                engine = team
                time = plain(p.contents[5])
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
                    qtime = str(60 * mins + seconds + etc)
                    delta = Decimal(qtime, 3) - Decimal(wtime, 3)
                    
                else:
                    delta = None
               
            elif len(p): 
                engine = plain(p.contents[5])
                if engine == 'Pratt &amp; Whitney':
                    engine = 'Pratt & Whitney'
                elif engine == 'K&#252;chen':
                    engine = 'Kuchen'
                time = plain(p.contents[7])
                tparts = time.split("'")
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
                    
                    qtime = str(60 * mins + seconds + etc)
                    delta = Decimal(qtime, 3) - Decimal(wtime, 3)
                    
                else:
                    delta = None
                    
        qtime = str(60 * mins + seconds + etc / 1000)
        qq = Decimal(qtime, 3)
        
        try:
            num, tyre = result[(first_name, family_name, team, engine)]
        except IndexError:
            num, tyre = 0, None
        print pos, num, first_name, family_name, team, engine, tyre, delta
  
#        r = Racer()
#        r.first_name = first_name
#        r.family_name = family_name
#        
#        qual = Result()
#        qual.heat = Heat.objects.get(grandprix=q.grandprix)
#        qual.position = pos
#        qual.num = num
#        qual.racer = Racer.objects.get(first_name=r.first_name, family_name=r.family_name)
#        qual.team = Team.objects.get(name=team)
#        qual.engine = Engine.objects.get(name=engine)
#        qual.tyre = Tyre.objects.get(name=tyre)
#        qual.delta = delta
#        qual.save()

        
        


def bestlap(opener, url):
    soup = readurl(opener, 'bestlap', url)
    tbody = soup.find('tbody')
    for tr in tbody.findAll('tr'):
        pos = tr.contents[1].contents[0]
        racer = plain(tr.contents[2])
        team = plain(tr.contents[3])
        engine = plain(tr.contents[4])
        time = plain(tr.contents[5])
        tparts = time.split("'")
        mins = int(tparts[0])
        seconds = int(tparts[1])
        try:
            etc = float(tparts[3]) / 1000.0
        except:
            etc = 0
        besttime = mins * 60 + seconds + etc        
        gap = plain(tr.contents[6])
        lap = plain(tr.contents[7])
        print pos, racer, team, engine, besttime, gap, lap
        



#Racers
def abcracer(opener, url):
    soup = readurl(opener, 'ABCRACER', url)
    div = soup.find('div', 'Alpha')
    for a in div.findAll('a'):
        if len(plain(a)) == 1 or plain(a) == 'F2':
            href = a['href']
            racerlist(opener, SITE + href)
            
def racerlist(opener, url):
    soup = readurl(opener, 'RACERLIST', url)
    table = soup.find('table', id='ctl00_CPH_Main_GV_Pilote')
    for tr in table.findAll('tr'):
        link = tr.contents[1]
        for a in link.findAll('a'):
            href = a['href']
            driver = plain(a)
            parts = driver.split(' ')
            first_name = plain(urlify(parts[0])).capitalize()
            
            first_name = plain(parts[-1])
            fname = first_name[0] + '.'
            family_name = plain(' '.join(parts[0:-1]))
#            racer(opener, SITE + href)
            print fname, family_name
            
def racer(opener, url):
    soup = readurl(opener, 'RACER', url)
    divname = soup.find('div', 'NavigCenter')
    divnation = soup.find('div', style='float:left;padding-right:20px;width:600px;')
    h1 = divname.find('h1')
    racer = plain(h1)
    parts = racer.split(' ')
    en_parts = []
    for i in range(0, len(parts)):
        family_parts = plain(urlify(parts[i].encode('utf-8').replace("'", '2').capitalize()).capitalize()) + ' '            
        en_parts.append(family_parts)
    first_name = plain(urlify(en_parts[0])).capitalize()
    family_name = plain(en_parts[1:])
    slug = urlify(family_name.lower())
    slug_details = urlify(first_name.lower() + '_' + family_name.lower())
    strong = divnation.find('strong')
    nation = plain(strong)
    asite = soup.find('a', id='ctl00_CPH_Main_HL_SiteWeb')
    if asite is None:
        website = None
    else:    
        site = asite['href']
        siteparts = asite['href'].split('://')
        website = siteparts[1] 
    date = plain(strong.nextSibling.nextSibling)
    parts = date.split(' ')
    if parts[2] == '?':
        day = 01
        month = 01
        year = 1700
    else:
        day = int(parts[2])
        month = MONTH.index(parts[3]) + 1
        year = int(parts[4])
        
    racer = Racer()
    racer.first_name = first_name
    racer.family_name = family_name
    racer.en_first_name = first_name
    racer.en_family_name = family_name
    if not Racer.objects.filter(family_name=family_name).count():
        racer.slug = slug
    else:
        racer.slug = slug_details
    racer.website = website
    racer.photo = 'upload/drivers/' + slug + '.jpg'
    racer.country = Country.objects.get(name=nation)
    racer.birthday = datetime.date(int(year), int(month), int(day))
    racer.save()

#    print 'First Name:', first_name
    print 'Family Name:', family_name
#    print 'Nation:', nation
#    print 'Date of birth:', datetime.date(year, month, day)
#    print 'Website:', website
#    print 'Slug:', slug


#Teams
def abcteam(opener, url):
    soup = readurl(opener, 'ABCTEAM', url)
    div = soup.find('div', 'Alpha')
    for a in div.findAll('a'):
        if len(plain(a)) == 1:
            href = a['href']
            teamlist(opener, SITE + href)
            
def teamlist(opener, url):
    soup = readurl(opener, 'TEAMLIST', url)
    table = soup.find('table', id='ctl00_CPH_Main_GV_Constructeur')
    for tr in table.findAll('tr'):
        link = tr.contents[1]       
        for a in link.findAll('a'):      
    	    href = a['href']
            team(opener, SITE + href)
            
def team(opener, url):
    soup = readurl(opener, 'TEAM', url)
    divname = soup.find('div', 'NavigCenter')
    h1 = divname.find('h1')
    name = plain(h1)
    founder = None
    divfounder = soup.find('div', style='margin-top:5px;')
    for strong in divfounder.find('strong'):    
        founder = plain(divfounder.contents[1])
    divnation = soup.find('div', style='float:left;min-width:500px;') 
    for strong in divnation.findAll('strong'):
        nation_name = plain(strong)
        parts = nation_name.split(' (')
        nation = parts[0]
    asite = soup.find('a', id='ctl00_CPH_Main_HL_SiteWeb')
    if asite is None:
        website = None
    else:    
        website = asite['href']

#    print 'Team:', team
#    print 'Founder:', founder
#    print 'Nation:', nation
#    print 'Website:', website
    
    team = Team()
    team.name = name
    team.en_name = name
    team.slug = urlify(name)
    team.founder = founder
    team.country = Country.objects.get(name=nation)
    team.website = website
    team.save()

   

#Engines
def abcengine(opener, url):
    soup = readurl(opener, 'ABCENGINE', url)
    div = soup.find('div', 'Alpha')
    for a in div.findAll('a'):
        if len(plain(a)) == 1:
            href = a['href']
            enginelist(opener, SITE + href)
            
def enginelist(opener, url):
    soup = readurl(opener, 'ENGINELIST', url)
    table = soup.find('table', id='ctl00_CPH_Main_GV_Moteur')
    for tr in table.findAll('tr'):
        link = tr.contents[1]       
        for a in link.findAll('a'):      
    	    href = a['href']
            engine(opener, SITE + href)

def engine(opener, url):
    soup = readurl(opener, 'ENGINE', url)
    divname = soup.find('div', 'NavigCenter')
    h1 = divname.find('h1')
    name = plain(h1)
    founder = None
    divfounder = soup.find('div', style='margin-top:5px;')
    for strong in divfounder.find('strong'):    
        founder = plain(divfounder.contents[1])
    divnation = soup.find('div', style='float:left;min-width:500px;') 
    for strong in divnation.findAll('strong'):
        nation_name = plain(strong)
        parts = nation_name.split(' (')
        nation = parts[0]
    asite = soup.find('a', id='ctl00_CPH_Main_HL_SiteWeb')
    if asite is None:
        website = None
    else:
        website = asite['href']
        
    engine = Engine()
    engine.name = name
    engine.en_name = name
    engine.slug = urlify(name)
    engine.founder = founder
    engine.country = Country.objects.get(name=nation)
    engine.website = website
    engine.save()
        
            #print engine, founder, nation, website

#Tracks
def tracklist(opener, url):
    soup = readurl(opener, 'TRACKLIST', url)
    table = soup.find('table', id='ctl00_CPH_Main_GV_Circuit')
    for tr in table.findAll('tr'):
        link = tr.contents[1]       
        for a in link.findAll('a'):      
    	    href = a['href']
            track(opener, SITE + href)


def track(opener, url):
    soup = readurl(opener, 'TRACK', url)
    maintable = soup.find('table', id='ctl00_CPH_Main_TBL_Version')
    lenall = []
    divname = soup.find('div', 'NavigCenter')    
    name = plain(divname.find('h1'))
    if name == 'New Delhi':
        length = 0
        lengths = []
    asite = soup.find('a', id='ctl00_CPH_Main_Hl_SiteWeb')
    if asite is None:
        website = None
    else:
        website = asite['href']
    maps = soup.find('a', id='ctl00_CPH_Main_HL_Google')
    if maps is None:
        googlemaps = None
    else:
        googlemaps = maps['href']
    
    track = Track()
    track.name = name
    track.en_name = name
    track.slug = urlify(name)
    track.website = website
    track.googlemaps = googlemaps
    track.save()
    if name != 'New Delhi':
        tracklen(opener, url)
    
#    print name
#    print slug
#    print website
#    for i in range(0,len(lengths)):
#        print lengths[i]
#    print googlemaps

def tracklen(opener, url):
    soup = readurl(opener, 'TRACKLEN', url)
    maintable = soup.find('table', id='ctl00_CPH_Main_TBL_Version')
    divname = soup.find('div', 'NavigCenter')    
    name = plain(divname.find('h1'))
    lenall = []
    for table in maintable.findAll('table', cellpadding="0"):
        for tr in table.findAll('tr')[1:]:
            length_str = plain(tr.contents[4])
            lparts = length_str.split('.')
            temp_km = lparts[0] + lparts[1]
            length_int = int(temp_km)
            length = int(length_int)
            if length == 'L (km)':
                continue
            lenall.append(length)
            lengths = []
            for a in lenall:
                if a not in lengths:
                    lengths.append(a)
    
    for i in range(0, len(lengths)):
        test = lengths[i]
        tracklen = TrackLen()
        tracklen.track = Track.objects.get(name=name)
        tracklen.photo = 'upload/tracks/' + urlify(name) + '-' + str(test) + '.png'
        tracklen.length = test
        tracklen.save()
        

#Nations
def abcnation(opener, url):
    soup = readurl(opener, 'ABCNATION', url)
    div = soup.find('div', 'Alpha')
    for a in div.findAll('a'):
        if len(plain(a)) == 1:
            href = a['href']
            nation(opener, SITE + href)
            
def nation(opener, url):
    soup = readurl(opener, 'NATIONLIST', url)
    table = soup.find('table', id='ctl00_CPH_Main_GV_Nation')
    for tr in table.findAll('tr'):
        nation = tr.contents[1]
        for a in nation.findAll('a'):
            nation_name = plain(a)
            filename = 'upload/flags/' + nation_name.lower() + '.png'
            if not Country.objects.filter(name=nation_name).count():
                #Country.objects.create(name=nation_name, photo=None)
                country = Country()
                country.name = nation_name
                country.en_name = nation_name
                country.photo = filename
                country.save()
                
                
                #team.founder = ''
                #team.country = Country.objects.get(name=country_name)
                #team.save()

def gpnation(opener, url):
    soup = readurl(opener, 'GPNATION', url)
    table = soup.find('table', id='ctl00_CPH_Main_GV_GrandPrix')
    for tr in table.findAll('tr'):
        link = tr.contents[1]       
        for a in link.findAll('a'):      
            gpnation = plain(a)
            print gpnation
            filename = 'upload/flags/' + gpnation.lower() + '.png'
            if not Country.objects.filter(name=gpnation).count():
                #Country.objects.create(name=nation_name, photo=None)
                country = Country()
                country.name = gpnation
                country.en_name = gpnation
                country.photo = filename
                country.save()
            

def main():

#    if os.sys.platform == 'win32':
#        os.system('CLS')
#    else:
#        os.system('clrscr')

    opener = urllib2.build_opener()

#    day = '12'
#    month = '2'
#    year = '1923'
#    racer.birthday = datetime.date(int(year), int(month), int(day))
#    datetime.datetime(int(year), int(month), int(day))


    #index(opener, SITE + '/en/saisons.aspx')
    #year(opener, 'http://statsf1.com/en/2010.aspx')
    #race(opener, 'http://statsf1.com/en/2010/monaco/classement.aspx')
    #grandprix(opener, 'http://statsf1.com/en/1950/indianapolis.aspx')
    #gplist(opener, 'http://statsf1.com/en/grands-prix.aspx')
    #entrans(opener, 'http://statsf1.com/en/1952/suisse/engages.aspx')
    #qual(opener, 'http://statsf1.com/en/2010/bahrein/grille.aspx')
    bestlap(opener, 'http://statsf1.com/en/2010/australie/meilleur-tour.aspx')
    #abcracer(opener, 'http://statsf1.com/en/pilotes.aspx')
    #racer(opener, 'http://statsf1.com/en/jean-pierre-beltoise.aspx')
    #abcteam(opener, 'http://statsf1.com/en/constructeurs.aspx')
    #team(opener, 'http://statsf1.com/en/ferrari.aspx')
    #abcengine(opener, 'http://statsf1.com/en/moteurs.aspx')
    #engine(opener, 'http://statsf1.com/en/moteur-renault.aspx')
    #tracklist(opener, 'http://statsf1.com/en/circuits.aspx')
    #track(opener, 'http://statsf1.com/en/circuit-yeongam.aspx')
    #tracklen(opener, 'http://statsf1.com/en/circuit-monaco.aspx')
    #abcnation(opener, 'http://statsf1.com/en/nations.aspx')
    #gpnation(opener, 'http://statsf1.com/en/grands-prix.aspx')

if __name__ == '__main__':
    main()
else:
    from f1info.models import *
