
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
  save_name = 'rets/' + name.split('/').pop()
  if os.path.exists(save_name) is True:
    return []
  if index%100 == 0:
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
  #return name, rets
  open(save_name, 'wb').write( gzip.compress(pickle.dumps(rets)))

allnames = []
names = glob.glob('./htmls/*.pkl.gz')
for index, name in enumerate(names):
  if re.search(r'read', name) is None:
    continue
  allnames.append((index,name)) 

if '--map1' in sys.argv:
  with concurrent.futures.ProcessPoolExecutor(max_workers=16) as exe: 
    exe.map(_map1, allnames)

if '--fold1' in sys.argv:
  f = open('mapped.jsonp', 'w')
  for name in glob.glob('rets/*.pkl.gz'):
    rets = pickle.loads( gzip.decompress( open(name, 'rb').read() ) )
    for ret in rets:
      f.write(ret + '\n')
     
