from beautifulsoup import BeautifulSoup, Tag
import re
import os
import urllib2
import datetime
from urltoracer import urls
from ractoracer import racs
from decimal import *

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


def index(opener, url):
    soup = readurl(opener, 'INDEX', url)
    table = soup.find('table', id='ctl00_CPH_Main_TBL_Annee')
    for a in table.findAll('a'):
        href = a['href']
        year(SITE + href)

def year(opener, url):
    soup = readurl(opener, 'YEAR', url)
    table = soup.find('table', id='ctl00_CPH_Main_TBL_GPSaison')
    for a in table.findAll('a'):
        href = a['href']
        grandprix(SITE + href)

def grandprix(opener, url):
    soup = readurl(opener, 'GRANDPRIX', url)
    meteo = soup.find('img', id='ctl00_CPH_Main_IMG_Meteo')
    td = meteo.parent.nextSibling.nextSibling
    # <td style="text-align:center;font-weight:bold;">  13 may...
    date = cut(td.contents[0])
    # u'13 may 1950 -'
    parts = date.split(' ')
    # [u'13', u'may', u'1950', u'-']
    day = int(parts[0])
    month = MONTH.index(parts[1]) + 1
    year = int(parts[2])

    info = cut(td.contents[3])
    # u'70 laps x 4.649 km - 325.430 km'
    parts = info.split(' ')
    # [u'70', u'laps', u'x', u'4.649', u'km', u'-', u'325.430', u'km']

    laps = int(parts[0])
    km = float(parts[3]) * 1000
    
    print 'Date:', day, month, year 
    print 'Laps:', laps
    print 'Track len:', km

    result = soup.find('a', id='ctl00_CPH_Main_HL_Classement')
    grid = soup.find('a', id='ctl00_CPH_Main_HL_Grille')
    best = soup.find('a', id='ctl00_CPH_Main_HL_MeilleurTour')
    reshref = result['href']
    gridhref = grid['href']
    besthref = best['href']
    #qual(SITE + gridhref)    
    #race(SITE + reshref)
    bestlap(SITE + besthref)

    

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
                    delta = Decimal(wtime, 3) - Decimal(qtime, 3)
                    
                else:
                    mins = None
                    seconds = None
                    etc = None
                    qq = None
               
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
                    delta = Decimal(wtime, 3) - Decimal(qtime, 3)
                    
                else:
                    mins = None
                    seconds = None
                    etc = None
                    qq = None
                    
        #global wtime
        
        #qtime = str(60*mins + seconds + etc/1000)
        #qq = Decimal(qtime, 3)
        print pos, racer, team, engine, delta
        
#        qual = Heat()
#        qual.grandprix = GrandPrix.objects.get(name='test')
#        qual.type = 'Q'
#        qual.date = datetime.datetime(int(2010), int(05), int(01))
#        qual.time = winnertime
#        qual.laps = 10
#        qual.slug = 'test'
#        qual.save()
#        
#        qual = Result()
#        qual.heat = Heat.objects.get(grandprix=1)
#        qual.position = pos
#        qual.racer = Racer.objects.get(en_name=en_name)
#        qual.team = Team.objects.get(name=team)
#        qual.engine = Engine.objects.get(name=engine)
#        qual.tyre = Tyre.objects.get(name='Bridgestone')
#        qual.delta = qq
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
            length_float = float(plain(tr.contents[4]))*1000
            length = int(length_float)
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
        
        
#    print name
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


    #index(SITE + '/en/saisons.aspx')
    #year('http://statsf1.com/en/1999.aspx')
    #race('http://statsf1.com/en/1993/europe/classement.aspx')
    qual(opener, 'http://statsf1.com/en/1997/europe/grille.aspx')
    #abcracer(opener, 'http://statsf1.com/en/pilotes.aspx')
    #racer(opener, 'http://statsf1.com/en/sebastien-buemi.aspx')
    #abcteam(opener, 'http://statsf1.com/en/constructeurs.aspx')
    #team(opener, 'http://statsf1.com/en/ferrari.aspx')
    #abcengine(opener, 'http://statsf1.com/en/moteurs.aspx')
    #engine(opener, 'http://statsf1.com/en/moteur-renault.aspx')
    #tracklist(opener, 'http://statsf1.com/en/circuits.aspx')
    #track(opener, 'http://statsf1.com/en/circuit-monaco.aspx')
    #tracklen(opener, 'http://statsf1.com/en/circuit-monaco.aspx')
    #abcnation(opener, 'http://statsf1.com/en/nations.aspx')

if __name__ == '__main__':
    main()
else:
    from f1info.models import *
