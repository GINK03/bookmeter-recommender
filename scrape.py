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

def _map1(arr):
  index, url = arr
  local_name = 'htmls/{}.pkl.gz'.format( url.replace('/', '_') )
  if os.path.exists(local_name):
    return url, None, None, None
  print('now scraping', url)
  try:
    headers = {
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:56.0) Gecko/20100101 Firefox/56.0',
    }
    #if random.random() < 0.5:
    proxy = proxys[index]
    print( proxy )
    req = requests.get(url, headers=headers, proxies=proxy )
    #else:
    #req = requests.get(url, headers=headers )
      
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
      if 'https://bookmeter.com/users' not in href:
        continue
      _links.append( href )
      print(href)
    local_name = 'htmls/{}.pkl.gz'.format( url.replace('/', '_') )
    open(local_name,'wb').write( gzip.compress(pickle.dumps( (req.text, _links ) )) )
    print('normaly done, ', url)
    time.sleep(1.0)
    return url, req.text, _links, None
  except Exception as e:
    print('Deep Error', e)
    # 原因となったproxyを削除する
    #proxys.remove(proxy)
    return url, None, None, None

#db = plyvel.DB('htmls.ldb', create_if_missing=True)
proxys = []
for line in open('aws_ip.txt'):
  line = line.strip()
  typed, ipaddr = line.split()
  proxys.append( {'http': '{}:8080'.format(ipaddr), 'https': '{}:8080'.format(ipaddr) } )
  print( {'http': '{}:8080'.format(ipaddr),  'https': '{}:8080'.format(ipaddr) } )

def scrape():
  links = ['https://bookmeter.com/users/1/books/read'] 
  if '--resume' in sys.argv:
    saveLinks = pickle.loads( gzip.decompress( open('saveLinks.pkl.gz', 'rb').read() ) )
    links = list(saveLinks)
  while True:
    if len(links) == 0:
      break
    arrs = [ (index%len(proxys), url) for index, url in enumerate(links) ]

    with concurrent.futures.ProcessPoolExecutor(max_workers=35) as exe:
      for url, html, _links, soup in exe.map( _map1, arrs):
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
    if index%1000 == 0:
      print('now iter', index, '/', size)
    try:
      html, _links = pickle.loads( gzip.decompress(open(filename, 'rb').read() ) )
    except Exception as e:
      continue
    for link in _links:
      href = link 
      try:
        if href[0] == '/':
          href = 'https://bookmeter.com' + href
      except IndexError:
        continue
      if 'https://bookmeter.com/users' not in href:
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
