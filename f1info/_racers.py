# -*- coding: utf-8 -*-
from beautifulsoup import BeautifulSoup, Tag
import re, os, urllib2, datetime
from urltoracer import urls
from ractoracer import racs
from syspts import *
from decimal import *
from urlify import *

SITE = 'http://statsf1.com'
MONTH = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', ]

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
    
def get_fuckin_name(list):
    f = ''
    for i in list[0:-1]:
        f = f + urlify(i).capitalize() + ' '
    return f    

# Racers
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
            #print urlify(parts[-1]).capitalize()
            #first_name = urlify(parts.latest).capitalize()
            #last_name = get_fuckin_name(parts)
            death(opener, SITE + href)
            #print '@' + href + '@' + ':' + '@' + first_name + ' ' + last_name + '@' + ','
            

def death(opener, url):
    soup = readurl(opener, 'RACER', url)
    part_url = url.split('http://statsf1.com')
    href = part_url[1]
    divname = soup.find('div', 'NavigCenter')
    divnation = soup.find('div', style='float:left;padding-right:20px;width:600px;')
    h1 = divname.find('h1')
    racer = plain(h1)
    parts = racer.split(' ')
    first_name = urlify(parts[0]).capitalize()
    last_name = get_last_name(parts)
    
    if divnation.find(text=re.compile('Die the')):
        dparts = divnation.find(text=re.compile('Die the')).split(' ')
        if dparts[3] == '?':
            day = 01
            month = 01
            year = 2100
        else:
            day = int(dparts[3])
            month = MONTH.index(dparts[4]) + 1
            year = int(dparts[5])
        
        #try:
        racer = Racer.objects.filter(first_name=first_name, family_name=last_name)
        print first_name, last_name
        print day, month, year
        racer.update(deathday = datetime.date(int(year), int(month), int(day)))
        #except:
        #    pass
    else:
        print 'pass'
        pass
    
    
    
    
            
def racer(opener, url):
    soup = readurl(opener, 'RACER', url)
    part_url = url.split('http://statsf1.com')
    href = part_url[1]
    divname = soup.find('div', 'NavigCenter')
    divnation = soup.find('div', style='float:left;padding-right:20px;width:600px;')
    h1 = divname.find('h1')
    racer = plain(h1)
    parts = racer.split(' ')
    first_name = urlify(parts[0]).capitalize()
    last_name = get_last_name(parts)
    slug = urlify(racer)
    strong = divnation.find('strong')
    nation = plain(strong)
    asite = soup.find('a', id='ctl00_CPH_Main_HL_SiteWeb')
    if asite is None:
        website = None
    else:    
        website = asite['href']
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
    
    print '@' + href + '@' + ':' + '@' + first_name + ' ' + last_name + '@' + ','

#    racer = Racer()
#    racer.first_name = first_name
#    racer.family_name = last_name
#    racer.en_first_name = first_name
#    racer.en_family_name = last_name
#    racer.slug = slug
#    racer.website = website
#    racer.photo = 'upload/drivers/' + slug + '.jpg'
#    racer.country = Country.objects.get(name=nation)
#    racer.birthday = datetime.date(int(year), int(month), int(day))
#    racer.save()

def main():
    opener = urllib2.build_opener() #proxy_handler, proxy_auth_handler)

    abcracer(opener, 'http://statsf1.com/en/pilotes.aspx')
    #racer(opener, 'http://statsf1.com/en/tom-belso.aspx')
    #death(opener, 'http://statsf1.com/en/red-amick.aspx')

if __name__ == '__main__':
    main()
else:
    from f1info.models import *
