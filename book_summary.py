import glob


import pickle

import gzip

import json

import bs4

import re

import sys

import os

import concurrent.futures 
if '--poll' in sys.argv:

  def _map1(arr):
    index, names = arr

    for name in names:
      try:
        html, links = pickle.loads( gzip.decompress( open(name, 'rb').read() ) )
      except:
        continue
      soup = bs4.BeautifulSoup(html)
      title = soup.find('h1', {'class':'inner__title'})
      summary = soup.find('div', {'class':'book-summary__default'}) 
      if title is None or summary is None:
        continue
      title = title.text
      if os.path.exists('summaries/{}.json'.format(title.replace('/', '_'))) is True:
        continue
      summary = summary.text
      print( name)
      print(title)

      print( summary )
      
      try:
        open('summaries/{}.json'.format(title.replace('/', '_')), 'w').write( json.dumps({'name':name, 'title':title, 'summary':summary}, indent=2, ensure_ascii=False))
      except Exception:
        continue
  while True:
    arrs = {} 
    for index, name in enumerate(glob.glob('htmls/*')):
      if 'bookmeter.com_books_' in name:
        key = index%8
        if arrs.get(key) is None:
          arrs[key] = []
        arrs[key].append( name )
    arrs = [ (index, names) for index, names in arrs.items()] 
    with concurrent.futures.ProcessPoolExecutor(max_workers=8) as exe:
      exe.map(_map1, arrs)
      
    
