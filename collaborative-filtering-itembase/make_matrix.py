import gzip

import pickle

import numpy as np

import sys

import copy

import concurrent.futures 

import json

import os
if '--step1' in sys.argv:
  key_pair = pickle.loads( gzip.decompress(open('../tmp/key_pair.pkl.gz', 'rb').read()) )

  book_users = {}
  for key, pair in key_pair.items():
    books = pair['books']
    
    for book in books:
      if book_users.get(book) is None:
        book_users[book] = set()
      book_users[book].add(key)
  open('book_users.pkl', 'wb').write( pickle.dumps(book_users) )

if '--step2' in sys.argv:
  def _map1(arr):
    #user_books = pickle.loads(open('user_books.pkl', 'rb').read() )
    #book_index = pickle.loads(open('book_index.pkl', 'rb').read() )
    _book_users = pickle.loads(open('book_users.pkl', 'rb').read() )
    for book, users in arr:
      if os.path.exists('book_book/{}.json'.format(book.replace('/', '_'))) is True:
        print('already processed', book)
        continue
      print( 'now scan', book )
      # あるユーザから、特定のユーザの読んだ本の集合の積が大きい順top 10を保存
      book_simil = {}
      for _book, _users in _book_users.items():
        book_simil[_book] = len(users & _users) / (len(users) * len(_users))**0.5
      
      book_simil = { _book: simil  for _book, simil in sorted(book_simil.items(), key=lambda x:x[1]*-1)[:21] }
      
      open('book_book/{}.json'.format(book.replace('/', '_')), 'w').write( json.dumps(book_simil, indent=2, ensure_ascii=False) )

 
  book_users = pickle.loads(open('book_users.pkl', 'rb').read() )
  arrs = {}
  for index, (book, users) in enumerate(book_users.items()):
    if arrs.get(index%16) is None:
      arrs[index%16] = []
    arrs[index%16].append( (book, users) )

  arrs = [ val for key, val in arrs.items() ]
  #_map1(arrs[0])

  with concurrent.futures.ProcessPoolExecutor(max_workers=8) as exe:
    exe.map(_map1, arrs)
