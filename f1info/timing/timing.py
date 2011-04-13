from optparse import OptionParser
import cookielib, urllib2, urllib
import logging
import time
import socket

class ParseException(Exception):
  pass

HOST = 'live-timing.formula1.com'
BASE_URL = 'http://live-timing.formula1.com'
AUTH_URL = "http://www.formula1.com/reg/login"
COOKIE_FILE = "cookies.txt"

class f1crypt(object):
  DEFAULT_MASK = 1431655765
  def __init__(self,key):
    self.key = key
    self.mask = self.DEFAULT_MASK;
    
  def set_key(self,key):
    self.key = key
    self.mask = self.DEFAULT_MASK;
  
  def reset(self):
    self.mask = self.DEFAULT_MASK;
  
  def decrypt(self,b):
    if self.key == 0:
      return b

    self.mask = (((self.mask >> 1) & 0x7fffffff) ^ (self.key if (self.mask&1) else 0))

    return ((b ^ self.mask) & 0xff)

class f1process(object):
 
  KEY_FRAME_URL = "http://live-timing.formula1.com/keyframe"
  MAX_COLS = 14

  RACEMODE_RACE	= 1
  RACEMODE_PRACTICE = 2
  RACEMODE_QUALIFYING = 3
  RACEMODE_QUALIFYING1 = 4
  RACEMODE_QUALIFYING2 = 5
 
  def __init__(self,app):
    self.app = app
    self.key_frame_cnt = 0
    self.key_frame_nr = -1
    self.loading_keyframe = False
    self.data=[]
    self.last_comment = ''
    self.racemode = self.RACEMODE_RACE
    for i in range(20):
      self.data.append([i+1]+['']*(self.MAX_COLS))
    self.fastest_lap = {}
    
  def format_row(self,row):
    if self.racemode == self.RACEMODE_RACE:
      return "%2s %2s %15s  %4s  %4s  %8s  %4s %0s %4s %0s %4s %2s %s %s"%tuple(row[1:])      
    else:
      return "%2s %2s %15s  %8s  %8s  %8s  %4s  %4s  %4s  %2s %s %s %s %s"%tuple(row[1:])

  def draw(self):
    s = sorted(self.data,lambda a,b:a[0]-b[0])

    board = '\n'.join(filter(lambda row:row.strip()!='',map(lambda row:self.format_row(row),s)))
    if board:
      print board,'\n'
    
  def get_bytes(self,nr,decrypt = False):
    ret = map(ord,self.stream.read(nr))
    if decrypt:
      ret = map(self.app.decrypter.decrypt,ret)
      
    return ret

  def get_string(self,nr,decrypt = False):
    return ''.join(map(chr,self.get_bytes(nr,decrypt)))

  def get_keyframe_url(self,n):
    if not n:
      url = "%s.bin"%(self.KEY_FRAME_URL)
      if self.key_frame_cnt:
        url+=("?%d"%self.key_frame_cnt)
    else:
      url = "%s_%05d.bin"%(self.KEY_FRAME_URL,n)
      self.key_frame_cnt = 0
    return url

  def load_keyframe(self,n = 0,stream = None):
    if n>self.key_frame_nr:
      self.loading_keyframe = True
      url = self.get_keyframe_url(n)
      logging.debug("loading keyframe %d from %s",n,url)

      self.process(self.app.urlopen(url))
      self.key_frame_nr = n
      if n:
        self.draw()
      self.loading_keyframe = False      
    else:
      logging.debug("keyframe %d was already loaded",n)
    return True

  def blip(self, msg):
    global blip
    try:
      if blip and not self.loading_keyframe:
        blip.status_create(msg)
    except Exception, e:
      logging.error(e)

  def process(self,stream):
    self.stream = stream
    while True:
      try:
        b1,b2 = self.get_bytes(2)
      except ValueError, e:
        return
      
      id = b1&0x1f
      x = (((b1 & 0xe0) >> 5)&0x07) | ((b2 & 0x1)<<3)
      c = (b2 & 0xe) >>1
      l = (b2 & 0xf0) >> 4
      v = (b2 & 0xfe) >> 1
      logging.debug("id:%d, x:%d, c:%d, l:%d, v:%d",id,x,c,l,v)
      if id>0:
        if x == 0:
          if v == 0:
            logging.debug("positions[%d] = %d",id,v)
            self.data[id-1][0] = v
          else:
            logging.debug("positions[%d] = %d",id,v)                        
            self.data[id-1][0] = v
        elif x==15:
          bytes = self.get_bytes(v,True)
          logging.debug("init row: %s",repr(bytes))
        else:
          if x<self.MAX_COLS:
            logging.debug('colors[%d][%d] == %d',id,x,c)
          if l<15:
            if l == 0:
              logging.debug('data[%d][%d] == null',id,x)
              self.data[id-1][x] = ''
            else:
              s = self.get_string(l,True)
              if x<self.MAX_COLS:
                pass
              logging.debug('data[%d][%d] = %s',id,x,repr(s))
              self.data[id-1][x] = s
      else:
        if x in (0,8):
          raise ParseException('Invalid domino in stream')
        elif x==1:
          s = self.get_string(l)
          logging.debug("session id:%s, racemode:%s",s[1:],c)
          self.app.session_id = s[1:]
          self.racemode = c
        elif x==2:
          bytes = self.get_bytes(l, decrypt = False)
          kf = (bytes[1] << 8) | bytes[0]
          logging.debug("kf: %s",kf)

          self.app.last_keyframe = kf
          if not self.loading_keyframe and self.key_frame_nr<=0:
            self.load_keyframe(kf)
            
          self.app.decrypter.reset()
        elif x==3:
          assert(l==0)
          logging.debug("valid marker: %s",c!=0)
        elif x==4:
          comment = self.get_string(v, decrypt = True)
          if ord(comment[0])<32:
            b1 = ord(comment[1])
            if b1&2:
              self.last_comment += comment[2:].decode('utf-16le')
            else:
              self.last_comment += comment[2:].decode('utf-8')
            if b1&1:
              logging.info("comment: %s",self.last_comment)
              self.blip(self.last_comment)
              self.last_comment = ''
          else:
            logging.info("Old-style comment: %s",comment)
        elif x==5:
          logging.debug("setting refresh to: %d",v)
        elif x==6:
          msg = self.get_string(v,decrypt = True)
          logging.debug("safety message: %s",msg)
        elif x==7:
          bytes = self.get_bytes(2, decrypt = True)
          ts = (bytes[1]<<8) | bytes[0] | (v<<16)&0xff0000;
#          logging.debug("Timestamp: %d",ts)
        elif x==9:
          if l<15:
            bytes = self.get_bytes(l, decrypt = True)
            if c>0:
#              logging.debug("Weather: c=%d, %s",c,''.join(map(chr,bytes)))
              pass
            elif l>0:
#              logging.debug("Session time:%s",''.join(map(chr,bytes)))
              pass
            
        elif x==10:
          string = self.get_string(v,decrypt = True)
          col = ord(string[0])
          datastr = string[1:]
          if col>=0 and col<=4:
            logging.debug("col:%d, datastr:%s",col,repr(datastr))
          else:
            """
INFO:root:Fastest lap column: 5, value:3
INFO:root:Fastest lap column: 6, value:F. MASSA
INFO:root:Fastest lap column: 7, value:1:15.154
INFO:root:Fastest lap column: 8, value:50
            """
            logging.info("Fastest lap column: %d, value:%s",col,datastr)          
            self.fastest_lap[col] = datastr
            if col==8:
              self.blip("BEST LAP: %s.%s %s ON LAP %s"%(self.fastest_lap[5],self.fastest_lap[6],self.fastest_lap[7],self.fastest_lap[8]))
        elif x==11:
          descr = self.get_string(l,decrypt = True)
          if c==1:
            logging.info("Race status: %s",descr)
          else:
            logging.info("Unknown misc status: %d",ord(descr[0]))
        elif x==12:
          s = self.get_string(v)
          logging.debug("nop, read %d bytes:%s",v,s)
        else:
          assert(0)

from threading import Thread

class stream(Thread):
  def __init__(self,app):
    Thread.__init__(self)
    self.app = app
    self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    self.sock.connect((HOST,4321))
    logging.debug('stream connected')
    self.sockfile = self.sock.makefile('r',0)
    self.start()
    
  def run(self):
    logging.debug("thread run")
    self.app.decrypter.reset()
    self.app.processor.process(self.sockfile)
    logging.debug("thread end")
    
  def ping(self):
    self.sock.send(chr(16))
  
  def terminate(self):
    self.sock.shutdown(socket.SHUT_RDWR)
#    self.sockfile.close()
#    self.sock.close()

class f1app(object):

  def __init__(self,delay = 1):
    self.decrypter = f1crypt(0)
    self._session_id = 0
    self.last_keyframe = 0
    self.delay = delay

    self.cookie_jar = cookielib.MozillaCookieJar()
    try:
      self.cookie_jar.load('cookies.txt')
      logging.debug('cookies loaded')
    except IOError,e:
      logging.debug(e)
    
    self.url_opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie_jar))

    
  def get_session_id(self):
    return self._session_id

  def set_session_id(self,value):
    self._session_id = value
    self.fetch_encryption_key()

  session_id = property(get_session_id, set_session_id)

  def fetch_encryption_key(self):
    key_url = "%s/reg/getkey/%s.asp?auth=%s"%(BASE_URL,self.session_id,self.auth_uid)
    logging.debug(key_url)
    data = self.urlopen(key_url).read()
    logging.debug("%s %s",key_url,data)
    if data.lower() == "invalid":
      logging.error("invalid credentials")
    else:
      key = eval('0x'+data)
      logging.debug('new encryption key: %x',key)
      self.decrypter = f1crypt(key)

  def terminate(self):
    self.stream.terminate()
    logging.debug('joining')
    self.stream.join()
    logging.debug('joined')

  def login(self,email,password):
    params = urllib.urlencode({'email':email, 'password':password})
    data = self.urlopen(AUTH_URL, params).read()
    if "liveTimingsApplet" in data:
      self.cookie_jar.save(COOKIE_FILE)
      return True

  def urlopen(self, path, params = None):
    return self.url_opener.open(path, params)

  def get_auth_uid(self):
    for cookie in self.cookie_jar:
      if cookie.domain.endswith('formula1.com') and cookie.name == 'USER':
        return cookie.value

  def process(self):
    self.auth_uid = self.get_auth_uid()
    if not self.auth_uid:
      logging.error('no credentials stored, provide email and password')
      return
      
    self.processor = f1process(self)
    self.fetch_encryption_key()

    while True:
      self.stream = stream(self)
      
      while self.stream.isAlive():
        self.stream.ping()
        self.processor.draw()
        time.sleep(self.delay)

      logging.debug('stream is not alive')
      
      while self.last_keyframe!=None:
        n = self.last_keyframe
        self.last_keyframe = None
        self.processor.load_keyframe(n)
        time.sleep(self.delay)

option_parser = OptionParser(usage="usage: %prog [options]")
option_parser.add_option("-u", "--user", dest = "user", help = "formula1.com user (email)")
option_parser.add_option("-p", "--password", dest = "password", help = "formula1.com password")
option_parser.add_option("-d", "--debug", dest = "debug", action = "store_true", help = "enables extra debug messages")
option_parser.add_option("-s", "--sleep", dest = "delay", default = 1, type="int", help = "refresh delay")

try:
  from blipapi import BlipApi
  option_parser.add_option("","--blipuser", default = "livetiming", dest = "blipuser", help = "blip user")
  option_parser.add_option("","--blippassword", dest = "blippassword", help = "blip password")
except Exception, e:
  logging.error('blip: %s',e)
  
(options, args) = option_parser.parse_args()

blip = BlipApi(options.blipuser, options.blippassword) if 'BlipApi' in locals() else None

logging.getLogger().setLevel(logging.DEBUG if options.debug else logging.INFO)

try:
  app = f1app(delay = options.delay)
  if options.user and options.password:
    if app.login(options.user,options.password):
      logging.info('logged in')
    else:
      logging.error('invalid credentials')
  app.process()
except KeyboardInterrupt, e:
  app.terminate()
  logging.debug('interrupted')
