import re, urllib2
from beautifulsoup import BeautifulSoup

SITE = 'http://statsf1.com'
MONTH = ['jan', 'feb', 'marth', 'april', 'may', 'june', 'july', 'aug', 'sep', 'oct', 'nov', 'des', ]

def cut(value):
  return (re.sub(r'(&nbsp;|\s)+', ' ', unicode(value))).strip()

def readurl(name, url):
  print '%s: %s' % (name, url)
  data = urllib2.urlopen(url).read()
  open('debug.html', 'w').write(data)
  return BeautifulSoup(data)
  

def index(url):
  soup = readurl('INDEX', url)
  table = soup.find('table', id='ctl00_CPH_Main_TBL_Annee')
  for a in table.findAll('a'):
    href = a['href']
    year(SITE + href)

def year(url):
  soup = readurl('YEAR', url)
  table = soup.find('table', id='ctl00_CPH_Main_TBL_GPSaison')
  for a in table.findAll('a'):
    href = a['href']
    grandprix(SITE + href)

def grandprix(url):
  soup = readurl('GRANDPRIX', url)
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

  print day, month, year, laps, km
  print td.contents[1]['href']

def test(url):
  soup = readurl('test', url)
  table = soup.find('table', id='ctl00_CPH_Main_GV_Stats')
  for tr in table.findAll('tr'):
    pos = tr.contents[1].contents[0]
    num = tr.contents[2].contents[0]
    print pos, num

#index(SITE + '/en/saisons.aspx')
test('http://statsf1.com/en/1990/etats-unis/classement.aspx')

