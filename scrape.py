import requests
import bs4 
import math
import time
import sys
#import plyvel
import os

import pickle
import gzip

import concurrent.futures
from requests.auth import HTTPProxyAuth
import glob

import random
import json

def _map1(url):
  print('now scraping', url)
  try:
    headers = {
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:56.0) Gecko/20100101 Firefox/56.0',
    }
    #if random.random() < 0.5:
    #proxy = random.choice( proxys )
    #req = requests.get(url, proxies=proxy )
    #else:
    req = requests.get(url, headers=headers )
      
    if( req.status_code != 200 ):
      print('status code', req.status_code )
      return url, None, None, None

    soup = bs4.BeautifulSoup( req.text, 'lxml' )
    
    _links = []
    for link in soup.find_all('a', href=True):
      href = link['href'] 
      try:
        if href[0] == '/':
          href = 'https://bookmeter.com' + href
      except IndexError:
        continue
      if 'https://bookmeter.com/users' not in href or 'read' not in href:
        continue
      _links.append( href )
      print(href)
    local_name = 'htmls/{}.pkl.gz'.format( url.replace('/', '_') )
    open(local_name,'wb').write( gzip.compress(pickle.dumps( (req.text, _links ) )) )
    print('normaly done, ', url)
    return url, req.text, _links, None
  except Exception as e:
    print('Deep Error', e)
    # 原因となったproxyを削除する
    #proxys.remove(proxy)
    return url, None, None, None

#db = plyvel.DB('htmls.ldb', create_if_missing=True)
proxys = []
for triple in json.loads(open('misc/proxies.json').read() ):
  ip, port, cn = triple
  proxys.append( {'https': '{ip}:{port}'.format(ip=ip,port=port)} )

def scrape():
  links = ['https://bookmeter.com/users/1/books/read'] 
  if '--resume' in sys.argv:
    saveLinks = pickle.loads( gzip.decompress( open('saveLinks.pkl.gz', 'rb').read() ) )
    links = list(saveLinks)
  while True:
    if len(links) == 0:
      break
    urls = links

    with concurrent.futures.ProcessPoolExecutor(max_workers=1) as exe:
      for url, html, _links, soup in exe.map( _map1, urls):
        if html is None:
          continue # dbにも入れない
        #db.put(bytes(url,'utf8'), gzip.compress(pickle.dumps( (html, _links ) )))
        links.remove(url)
        open('tmp/finished/' + url.replace('/','_'), 'a' )
        for _link in _links:
          #if db.get(bytes(_link, 'utf8')) is not None:
          #  continue
          if os.path.exists('tmp/finished/' + url.replace('/','_')) is True:
            continue
          print('find new link', _link)
          links.append( _link )

    #time.sleep(0.1)
    break

def dump():
  links = set()
  arrs = [(index, filename) for index, filename in enumerate(glob.glob('htmls/*'))]
  size = len(arrs)

  alreadies = set([])
  for index, filename in arrs:
    url = filename.split('/').pop().replace('_', '/')
    alreadies.add( url )
  for index, filename in arrs: 
    print('now iter', index, '/', size)
    html, _links = pickle.loads( gzip.decompress(open(filename, 'rb').read() ) )
    for link in _links:
      href = link 
      try:
        if href[0] == '/':
          href = 'https://bookmeter.com' + href
      except IndexError:
        continue
      if 'https://bookmeter.com/users' not in href or 'read' not in href:
        continue
      links.add( href )
      #print(links)
  
  saveLinks = []
  for link in links:
    if link not in alreadies:
      saveLinks.append(link)
  print(saveLinks)
  open('saveLinks.pkl.gz', 'wb').write( gzip.compress(pickle.dumps(saveLinks)) ) 

if '--scrape' in sys.argv:
  scrape()

if '--dump' in sys.argv: 
  dump()
