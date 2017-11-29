import glob


import pickle

import gzip

import json

import bs4

import re

import sys

if '--poll' in sys.argv:
  while True:
    for name in glob.glob('htmls/*'):
      if 'bookmeter.com_books_' in name:
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
        summary = summary.text
        print( name)
        print(title)

        print( summary )
        
        try:
          open('sammaries/{}.json'.format(title.replace('/', '_')), 'w').write( json.dumps({'name':name, 'title':title, 'summary':summary}, indent=2, ensure_ascii=False))
        except Exception:
          continue
