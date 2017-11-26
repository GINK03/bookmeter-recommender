import gzip

import pickle

import numpy as np

import sys

if '--step1' in sys.argv:
  key_pair = pickle.loads( gzip.decompress(open('../tmp/key_pair.pkl.gz', 'rb').read()) )

  user_books = {}
  for key, pair in key_pair.items():
    user_books[key] = pair['books']

  open('user_books.pkl', 'wb').write( pickle.dumps(user_books) )
  book_index = {}
  for user, books in user_books.items():
    for book in books:
      if book_index.get(book) is None:
        book_index[book] = len(book_index)
  open('book_index.pkl', 'wb').write( pickle.dumps(book_index) )

import copy

import concurrent.futures 

import json
if '--step2' in sys.argv:
  def _map1(arr):
    #user_books = pickle.loads(open('user_books.pkl', 'rb').read() )
    #book_index = pickle.loads(open('book_index.pkl', 'rb').read() )
    _user_books = pickle.loads(open('user_books.pkl', 'rb').read() )
    for user, books in arr:
      print( 'now scan', user )
      # あるユーザから、特定のユーザの読んだ本の集合の積が大きい順top 10を保存
      user_simil = {}
      for _user, _books in _user_books.items():
        user_simil[_user] = len(books & _books)
      
      user_simil = { _user: simil  for _user, simil in sorted(user_simil.items(), key=lambda x:x[1]*-1)[:21] }
      
      open('user_user/{}.json'.format(user.replace('/', '_')), 'w').write( json.dumps(user_simil, indent=2, ensure_ascii=False) )

 
  user_books = pickle.loads(open('user_books.pkl', 'rb').read() )
  arrs = {}
  for index, (user, books) in enumerate(user_books.items()):
    if arrs.get(index%16) is None:
      arrs[index%16] = []
    arrs[index%16].append( (user, books) )

  arrs = [ val for key, val in arrs.items() ]
  #_map1(arrs[0])
  with concurrent.futures.ProcessPoolExecutor(max_workers=8) as exe:
    exe.map( _map1, arrs )
