
import os

import sys

import bs4
import json
import pickle
import gzip
import re

import glob

names = glob.glob('./htmls/*.pkl.gz')
for name in names:
  name
  
  if re.search(r'read', name) is None:
    continue
  
  #print(key)
  html, links = pickle.loads(gzip.decompress( open(name,'rb').read() ))
  #print( html )
  soup = bs4.BeautifulSoup(html)

  user_name = soup.find('div', {'class':'userdata-side__name'}).text
  user_id   = re.search(r'/(\d{1,})/', soup.find('meta', {'property':'og:url'})['content']).group(1)
  #user_id   = re.search(r'/(\d{1,})/', key).group(1)

  name_id = '{}_{}'.format(user_name, user_id)
  for div in soup.find_all('div', {'class':'book__detail'}):
    title = div.find('div', {'class':'detail__title'}).text
    page  = div.find('div', {'class':'detail__page'}).text
    date  = div.find('div', {'class':'detail__date'}).text
    obj = {'title':title, 'page':page, 'date':date}
    print(name_id + '\t' + json.dumps(obj, ensure_ascii=False) )

