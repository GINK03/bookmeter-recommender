import plyvel

import os

import sys

import bs4
import json
import pickle
import gzip
import re

db = plyvel.DB('htmls.ldb.b')
for key,val in db:
  key = key.decode('utf8')
  
  if re.search(r'read', key) is None:
    continue
  
  #print(key)
  html, links = pickle.loads(gzip.decompress(val))
  soup = bs4.BeautifulSoup(html)

  user_name = soup.find('div', {'class':'userdata-side__name'}).text
  user_id   = re.search(r'/(\d{1,})/', key).group(1)

  name_id = '{}_{}'.format(user_name, user_id)
  for div in soup.find_all('div', {'class':'book__detail'}):
    title = div.find('div', {'class':'detail__title'}).text
    page  = div.find('div', {'class':'detail__page'}).text
    date  = div.find('div', {'class':'detail__date'}).text
    obj = {'title':title, 'page':page, 'date':date}
    print(name_id + '\t' + json.dumps(obj, ensure_ascii=False) )

