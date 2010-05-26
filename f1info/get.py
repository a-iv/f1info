from beautifulsoup import BeautifulSoup, Tag
import re
import os
import urllib2
import datetime
from urltoracer import urls
from ractoracer import racs
from syspts import *
from decimal import *

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


def index(opener, url):
    soup = readurl(opener, 'INDEX', url)
    table = soup.find('table', id='ctl00_CPH_Main_TBL_Annee')
    for a in table.findAll('a'):
        season = plain(a)
        index = Season() 
        index.year = season
        index.save()
        href = a['href']
        year(opener, SITE + href)

def year(opener, url):
    soup = readurl(opener, 'YEAR', url)
    divname = soup.find('div', 'NavigCenter')
    h1 = divname.find('h1')
    season = int(plain(h1))
    table = soup.find('table', id='ctl00_CPH_Main_TBL_GPSaison')
    if season >= 1950 and season <= 1959:
        for i in range(1, len(pts50)+1):
            point = Point()
            point.season = Season.objects.get(year=season)
            point.position = i
            point.point = getPts50(i)
            point.save()
    if season == 1960:
        for i in range(1, len(pts60)+1):
            point = Point()
            point.season = Season.objects.get(year=season)
            point.position = i
            point.point = getPts60(i)
            point.save()
    if season >= 1961 and season <= 1990:
        for i in range(1, len(pts61)+1):
            point = Point()
            point.season = Season.objects.get(year=season)
            point.position = i
            point.point = getPts61(i)
            point.save()
    if season >= 1991 and season <= 2002:
        for i in range(1, len(pts91)+1):
            point = Point()
            point.season = Season.objects.get(year=season)
            point.position = i
            point.point = getPts91(i)
            point.save()    
    if season >= 2003 and season <= 2009:
        for i in range(1, len(pts03)+1):
            point = Point()
            point.season = Season.objects.get(year=season)
            point.position = i
            point.point = getPts03(i)
            point.save()
    if year == 2010:
        for i in range(1, len(pts10)+1):
            point = Point()
            point.season = Season.objects.get(year=season)
            point.position = i
            point.point = getPts10(i)
            point.save()
               

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
    slug = (name + '-' + season).lower()
    try:
        season_t = parts[3]
        slug = (name + '-' + season_t).lower()
    except:
        None
    
    # <td style="text-align:center;font-weight:bold;">  13 may...
    track = plain(td.contents[1])
    date = cut(td.contents[0])
    # u'13 may 1950 -'
    dparts = date.split(' ')
    # [u'13', u'may', u'1950', u'-']
    day = int(dparts[0])
    month = MONTH.index(dparts[1]) + 1
    year = int(dparts[2])

    info = cut(td.contents[3])
    # u'70 laps x 4.649 km - 325.430 km'
    kparts = info.split(' ')
    # [u'70', u'laps', u'x', u'4.649', u'km', u'-', u'325.430', u'km']

    laps = int(kparts[0])
    len = kparts[3]
    lparts = len.split('.')
    temp_km = lparts[0] + lparts[1]
    km = int(temp_km)
#    print km
    
#    print index
#    print name
#    print season
#    print track
#    print 'Date:', day, month, year 
#    print 'Laps:', laps
#    print 'Track len:', km

    #result = soup.find('a', id='ctl00_CPH_Main_HL_Classement')
    #grid = soup.find('a', id='ctl00_CPH_Main_HL_Grille')
    #best = soup.find('a', id='ctl00_CPH_Main_HL_MeilleurTour')
    #reshref = result['href']
    #gridhref = grid['href']
    #besthref = best['href']
    #qual(opener, SITE + gridhref)    
    #race(SITE + reshref)
    #bestlap(SITE + besthref)
    
    
    
    #print track
    #print km
    test = TrackLen()
    test.track = Track.objects.get(name=track)
    fail = Track()
    fail.tracklen = TrackLen.objects.get(track=test.track, length=km)
    #print test.track
    #print fail.tracklen
    
    
    grandprix = GrandPrix()
    grandprix.index = index
    try:
        grandprix.season = Season.objects.get(year=season)
    except:
        grandprix.season = Season.objects.get(year=season_t)
    grandprix.name = GPName.objects.get(name=name)
    grandprix.abbr = ''
    grandprix.slug = slug
    try:
        grandprix.country = Country.objects.get(name=country)
    except:
        grandprix.country = Country.objects.get(name='Unknown')
    grandprix.tracklen = fail.tracklen
    grandprix.save()
    
    

        

    
def gplist(opener, url):
    soup = readurl(opener, 'GPLIST', url)
    table = soup.find('table', id='ctl00_CPH_Main_GV_GrandPrix')
    for tr in table.findAll('tr'):
        link = tr.contents[1]       
        for a in link.findAll('a'):      
            link = plain(a)
            gplist = GPName()
            gplist.name = link
            gplist.save()
            
        
        
#Race
def race(opener, url):
    soup = readurl(opener, 'race', url)
    tbody = soup.find('tbody')
    for tr in tbody.findAll('tr')[0:1]:
        result = plain(tr.contents[7])
        rparts = result.split(' ')
        tmp_hours = rparts[0]
        hparts = tmp_hours.split('h')
        hours = int(hparts[0])
        tmp_minutes = rparts[1]
        mparts = tmp_minutes.split('m')
        minutes = int(mparts[0])
        tmp_etc = rparts[2]
        sparts = tmp_etc.split('s')
        etc = float(sparts[0])
        wintime = float(hours*3600 + minutes*60 + etc)
    print 'Winner time:', wintime        
    for tr in tbody.findAll('tr'):
        #try:
        #    num = int(tr.contents[2].contents[0])
        #except:
        #    continue
        #try:        
        #    pos = int(tr.contents[1].contents[0])
        #except:
        #    pos += 1        
        pos = tr.contents[1].contents[0]
        num = tr.contents[2].contents[0]
        racer = plain(tr.contents[3])
        team = plain(tr.contents[4])
        engine = plain(tr.contents[5])
        lap = tr.contents[6].contents[0]
        result = plain(tr.contents[7])
        rparts = result.split(' ')
        if (len(rparts) > 4):
            tmp_hours = rparts[0]
            hparts = tmp_hours.split('h')
            hours = int(hparts[0])
            tmp_minutes = rparts[1]
            mparts = tmp_minutes.split('m')
            minutes = int(mparts[0])
            tmp_etc = rparts[2]
            sparts = tmp_etc.split('s')
            etc = float(sparts[0])
            res = abs(wintime - float(hours*3600 + minutes*60 + etc))
        else:
            res = result
        print pos, num, racer, team, engine, lap, res

#Starting grid
def qual(opener, url):
    soup = readurl(opener, 'qual', url)
    table = soup.find('table', id='ctl00_CPH_Main_TBL_Grille')
    wtime = 0
    slug = 0
    divname = soup.find('div', 'NavigCenter')
    h1 = divname.find('h1')
    for a in h1.find('a'):
        slug_t = plain(a).lower()
        slpart = slug_t.split(' ')
        slug = plain('-'.join(slpart[0:]))+'-q' 
    
    for p in table.findAll('p'):
        temp = plain(p)
        parts = temp.split('.')
        pos = parts[0]
        if p.find('strong'):
            if len(p) > 8: 
                href = p.contents[2]['href']
                racer = getRacer(href)
                parts = racer.split(' ')
                first_name = parts[0]
                fname = []
                for i in range(1,len(parts)):
                    fname_parts = (parts[i] + ' ').capitalize()            
                    fname.append(fname_parts)
                family_name =  plain(fname)
                en_name = first_name + ' ' + family_name
                team = plain(p.contents[4])
                engine = plain(p.contents[6])
                time = plain(p.contents[8])
                tparts = time.split("'")
                mins = int(tparts[0])
                seconds = int(tparts[1])
                try:
                    etc = float(tparts[3])
                except:
                    etc = 0
            #    wtime = str(60*mins + seconds + etc/1000)
                
            else:                 
                href = p.contents[2]['href']
                racer = getRacer(href)
                parts = racer.split(' ')
                first_name = parts[0]
                fname = []
                for i in range(1,len(parts)):
                    fname_parts = (parts[i] + ' ').capitalize()            
                    fname.append(fname_parts)
                family_name =  plain(fname) 
                en_name = first_name + ' ' + family_name         
                team = plain(p.contents[4])
                engine = team
                time = plain(p.contents[6])
                tparts = time.split("'")
                mins = int(tparts[0])
                seconds = int(tparts[1])
                try:
                    etc = float(tparts[3])
                except:
                    etc = 0
            wtime = str(60*mins + seconds + etc/1000)
        else:
            continue
        print pos, racer, team, engine, wtime
        
        
        
#        qual = Heat()
#        qual.grandprix = GrandPrix.objects.get(name='test')
#        qual.type = 'Q'
#        qual.date = datetime.datetime(int(2010), int(05), int(01))
#        qual.time = wtime
#        qual.laps = 0
#        qual.slug = slug
#        qual.save()
#        
#        qual = Result()
#        qual.heat = Heat.objects.get(grandprix=1)
#        qual.position = pos
#        qual.racer = Racer.objects.get(en_name=en_name)
#        qual.team = Team.objects.get(name=team)
#        qual.engine = Engine.objects.get(name=engine)
#        qual.tyre = Tyre.objects.get(name='Bridgestone')
#        qual.delta = 0
#        qual.save()
            
    for p in table.findAll('p'):
        temp = plain(p)
        parts = temp.split('.')
        pos = parts[0]
        if p.find('strong'):
            continue
        
        else: 
            href = p.contents[1]['href']
            racer = getRacer(href)
            parts = racer.split(' ')
            first_name = parts[0]
            fname = []
            for i in range(1,len(parts)):
                fname_parts = (parts[i] + ' ').capitalize()            
                fname.append(fname_parts)
            family_name =  plain(fname)
            en_name = first_name + ' ' + family_name
            team = plain(p.contents[3])
            if len(p) < 8: 
                engine = team
                time = plain(p.contents[5])
                if time: 
                    tparts = time.split("'")
                    mins = int(tparts[0])
                    seconds = int(tparts[1])
                    try:
                        etc = float(tparts[3])
                    except:
                        etc = 0
                    qtime = str(60*mins + seconds + etc/1000)
                    delta = Decimal(qtime, 3) - Decimal(wtime, 3)
                    
                else:
                    mins = None
                    seconds = None
                    etc = None
                    delta = 0
               
            elif len(p): 
                engine = plain(p.contents[5])
                time = plain(p.contents[7])
                tparts = time.split("'")
                if time:
                    tparts = time.split("'")
                    mins = int(tparts[0])
                    seconds = int(tparts[1])
                    try:
                        etc = float(tparts[3])
                    except:
                        etc = 0
                    
                    qtime = str(60*mins + seconds + etc/1000)
                    delta = Decimal(qtime, 3) - Decimal(wtime, 3)
                    
                else:
                    mins = None
                    seconds = None
                    etc = None
                    delta = 0
                    
        #global wtime
        
        #qtime = str(60*mins + seconds + etc/1000)
        #qq = Decimal(qtime, 3)
        #print pos, racer, team, engine, delta
        
        
#        qual = Result()
#        qual.heat = Heat.objects.get(grandprix=1)
#        qual.position = pos
#        qual.racer = Racer.objects.get(en_name=en_name)
#        qual.team = Team.objects.get(name=team)
#        qual.engine = Engine.objects.get(name=engine)
#        qual.tyre = Tyre.objects.get(name='Bridgestone')
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
            etc = float(tparts[3])/1000.0
        except:
            etc = 0
        besttime = mins*60 + seconds + etc        
        gap = plain(tr.contents[6])
        lap = plain(tr.contents[7])
        print pos, racer, team, engine, besttime, gap, lap
        



#Racers
def abcracer(opener, url):
    soup = readurl(opener, 'ABCRACER', url)
    div = soup.find('div', 'Alpha')
    for a in div.findAll('a'):
        if len(plain(a)) == 1:
            href = a['href']
            racerlist(opener, SITE + href)
            
def racerlist(opener, url):
    soup = readurl(opener, 'RACERLIST', url)
    table = soup.find('table', id='ctl00_CPH_Main_GV_Pilote')    
    for tr in table.findAll('tr'):
        link = tr.contents[1]       
        for a in link.findAll('a'):
            href = a['href']
#            driver = plain(a)
#            parts = driver.split(' ')
#            first_name = plain(parts[-1])
#            fname = first_name[0] + '.'
#            family_name = plain(' '.join(parts[0:-1]))   
            racer(opener, SITE + href)
#            print fname, family_name
            
def racer(opener, url):
    soup = readurl(opener, 'RACER', url)
    divname = soup.find('div', 'NavigCenter')
    divnation = soup.find('div', style='float:left;padding-right:20px;width:600px;')
    h1 = divname.find('h1')
    racer = plain(h1)
    parts = racer.split(' ')
    first_name = parts[0]
    fname = []
    for i in range(1,len(parts)):
        fname_parts = (parts[i] + ' ').capitalize()            
        fname.append(fname_parts)
    family_name =  plain(fname)
    en_name = first_name + ' ' + family_name
    slug = family_name.lower()
    slug_details = first_name.lower() + '_' + family_name.lower()
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
        year = 1800
    else:
        day = int(parts[2])
        month = MONTH.index(parts[3]) + 1
        year = int(parts[4])
        
#    racer = Racer()
#    racer.first_name = first_name
#    racer.family_name = family_name
#    racer.en_name = en_name
#    if not Racer.objects.filter(family_name=family_name).count():
#        racer.slug = slug
#    else:
#        racer.slug = slug_details
#    racer.website = website
#    racer.photo = 'upload/drivers/' + slug + '.jpg'
#    racer.country = Country.objects.get(name=nation)
#    racer.birthday = datetime.date(int(year), int(month), int(day))
#    racer.save()

    print 'Driver:', first_name, family_name
    print 'Nation:', nation
    print 'Date of birth:', datetime.date(year, month, day)
    print 'Website:', website


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
    slug = name.lower()
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
    team.slug = slug
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
    slug = name.lower()
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
    engine.slug = slug
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
    slug = name.lower()
    if name == 'Yeongam':
        length = 0
        lengths = []
    asite = soup.find('a', id='ctl00_CPH_Main_Hl_SiteWeb')
    if asite is None:
        website = None
    else:
        site = asite['href']
        siteparts = asite['href'].split('://')
        website = siteparts[1]
    maps = soup.find('a', id='ctl00_CPH_Main_HL_Google')
    if maps is None:
        googlemaps = None
    else:
        googlemaps = maps['href']
    
    
    track = Track()
    track.name = name
    track.slug = slug
    track.website = website
    track.googlemaps = googlemaps
    track.save()
    if name != 'Yeongam':
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
    
    for i in range(0,len(lengths)):
        test = lengths[i]
        tracklen = TrackLen()
        tracklen.track = Track.objects.get(name=name)
        tracklen.photo = None
        tracklen.length = test
        tracklen.save()
        
        
    #print name
#    for i in range(0,len(lengths)):
#        print lengths[i]

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
                country.photo = filename
                country.save()
                
                
                #team.founder = ''
                #team.country = Country.objects.get(name=country_name)
                #team.save()

def main():
    realm = 'Squid proxy-caching web server'
    host = 'proxy.hq.redsolution.ru:3128'
    user = 'alexey.kuligin'
    password = ''

#    if os.sys.platform == 'win32':
#        os.system('CLS')
#    else:
#        os.system('clrscr')

    proxy_handler = urllib2.ProxyHandler({'http': 'http://%s/' % host})
    proxy_auth_handler = urllib2.ProxyBasicAuthHandler()
    proxy_auth_handler.add_password(realm, host, user, password)
    opener = urllib2.build_opener() #proxy_handler, proxy_auth_handler)

#    day = '12'
#    month = '2'
#    year = '1923'
#    racer.birthday = datetime.date(int(year), int(month), int(day))
#    datetime.datetime(int(year), int(month), int(day))


    #index(opener, SITE + '/en/saisons.aspx')
    #year(opener, 'http://statsf1.com/en/2003.aspx')
    #race('http://statsf1.com/en/1993/europe/classement.aspx')
    #grandprix(opener, 'http://statsf1.com/en/1950/indianapolis.aspx')
    #gplist(opener, 'http://statsf1.com/en/grands-prix.aspx')
    qual(opener, 'http://statsf1.com/en/2010/monaco/grille.aspx')
    #abcracer(opener, 'http://statsf1.com/en/pilotes.aspx')
    #racer(opener, 'http://statsf1.com/en/sebastien-buemi.aspx')
    #abcteam(opener, 'http://statsf1.com/en/constructeurs.aspx')
    #team(opener, 'http://statsf1.com/en/ferrari.aspx')
    #abcengine(opener, 'http://statsf1.com/en/moteurs.aspx')
    #engine(opener, 'http://statsf1.com/en/moteur-renault.aspx')
    #tracklist(opener, 'http://statsf1.com/en/circuits.aspx')
    #track(opener, 'http://statsf1.com/en/circuit-yeongam.aspx')
    #tracklen(opener, 'http://statsf1.com/en/circuit-monaco.aspx')
    #abcnation(opener, 'http://statsf1.com/en/nations.aspx')

if __name__ == '__main__':
    main()
else:
    from f1info.models import *
