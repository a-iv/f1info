# -*- coding: utf-8 -*-

import re, urllib2
from beautifulsoup import BeautifulSoup, Tag
import datetime
import os
from urlify import *


SITE = 'http://statsf1.com/en/peter-st-chelin.aspx'

opener = urllib2.build_opener() #proxy_handler, proxy_auth_handler)
MONTH = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', ]


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

def readurl(opener, name, url):
    print '%s: %s' % (name, url)
    opened = opener.open(url)
    data = opened.read()
    open('debug.html', 'w').write(data)
    return BeautifulSoup(data)


def racer(opener, url):
    soup = readurl(opener, 'RACER', url)
    divname = soup.find('div', 'NavigCenter')
    divnation = soup.find('div', style='float:left;padding-right:20px;width:600px;')
    h1 = divname.find('h1')
    racer = plain(h1)
    parts = racer.split(' ')
    en_parts = []
    for i in range(0, len(parts) - 1):
        first_parts = plain(parts[i]).capitalize() + ' '            
        en_parts.append(first_parts)
    first_name = plain(en_parts)
    family_name = plain(parts[-1]).capitalize()
    en_name = first_name + ' ' + family_name
    slug = urlify(family_name.lower())
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
        

    print 'Driver:', first_name, family_name
    print 'Nation:', nation
    print 'Date of birth:', datetime.date(year, month, day)
    print 'Website:', website
    print 'Slug:', slug
  

racer(opener, SITE)


