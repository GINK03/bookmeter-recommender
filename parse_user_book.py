
import os

import sys

import bs4
import json
import pickle
import gzip
import re

import glob

import concurrent.futures

def _map1(arr):
  index, name = arr
  print('now iter', index, name, file=sys.stderr)
  
  try:
    html, links = pickle.loads(gzip.decompress( open(name,'rb').read() ))
  except Exception as e:
    return []
  #print( html )
  soup = bs4.BeautifulSoup(html)

  user_name = soup.find('div', {'class':'userdata-side__name'}).text
  user_id   = re.search(r'/(\d{1,})/', soup.find('meta', {'property':'og:url'})['content']).group(1)
  #user_id   = re.search(r'/(\d{1,})/', key).group(1)

  name_id = '{}_{}'.format(user_name, user_id)

  rets = []
  for div in soup.find_all('div', {'class':'book__detail'}):
    title = div.find('div', {'class':'detail__title'}).text
    page  = div.find('div', {'class':'detail__page'}).text
    date  = div.find('div', {'class':'detail__date'}).text
    obj = {'title':title, 'page':page, 'date':date}
    rets.append(name_id + '\t' + json.dumps(obj, ensure_ascii=False) )
  return rets

allnames = []
names = glob.glob('./htmls/*.pkl.gz')
for index, name in enumerate(names):
  if re.search(r'read', name) is None:
    continue
  allnames.append((index,name)) 

f = open('mapped.jsonp', 'w')
with concurrent.futures.ProcessPoolExecutor(max_workers=8) as exe:
  
  for rets in exe.map(_map1, allnames):
    for ret in rets:
      f.write( ret + '\n' )
