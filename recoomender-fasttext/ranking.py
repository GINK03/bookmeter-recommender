import numpy as np
import pickle
import gzip
import sys
import os
import json
import concurrent.futures 
import glob
if '--to_vec' in sys.argv:
  book_vec = {}
  for line in open('model.vec'):
    line = line.strip()
    es = line.split(' ')
    book = es.pop(0)
    vec = [float(v) for v in es]
    #print( book, vec )
    book_vec[book] = vec

  open('book_vec.pkl.gz', 'wb').write( gzip.compress(pickle.dumps(book_vec)) )


def _sim(arrs):
  arrs, index_book,  books, vecs = arrs
  allnorms = np.linalg.norm(vecs, axis=(1,) )
  book_sims = {}
  for i in  arrs:
    vec = vecs[i]
    book = books[i]
    if os.path.exists('sims/{}.json'.format(book)) is True:
      print('already processed', book)
      continue
    print( i, '/', size, book )
    norm = np.linalg.norm(vec)*allnorms
    invnorm = norm**-1
    x_wa = (vec * vecs).sum(axis=1) 
    sims = x_wa * invnorm
    sims = dict( sorted( [(index_book[index], sim) for index, sim in enumerate(sims.tolist())], key=lambda x:x[1]*-1 )[:128] )
    try:
      open('sims/{}.json'.format(book), 'w').write( json.dumps(sims, indent=2, ensure_ascii=False, sort_keys=True) )     
    except Exception as e:
      print(e)


if '--sim' in sys.argv:
  book_vec = pickle.loads( gzip.decompress(open('book_vec.pkl.gz', 'rb').read() ) )
  books = []
  vecs = []
  for book, vec in book_vec.items():
    vec = np.array(vec)
    if( (128,) != vec.shape ):
      continue
    books.append(book)
    vecs.append( vec)

  vecs = np.array(vecs)
  
  index_book = dict([(index, book) for index, book in enumerate(books)])

  open('index_book.json', 'w').write( json.dumps(index_book, indent=2, ensure_ascii=False) )
  print( vec.shape )
  size, weight = vecs.shape

  cur_data = {}
  for i in range(size):
    cur = i%16
    if cur_data.get(cur) is None:
      cur_data[cur] = []
    cur_data[cur].append( i )
  cur_data = [(arrs, index_book, books, vecs) for arrs in cur_data.values() ]
 
  #_sim( cur_data[0] )
  book_sims = {}
  with concurrent.futures.ProcessPoolExecutor(max_workers=16) as exe:
    exe.map( _sim, cur_data )

  open('book_sim.pkl.gz', 'wb').write( gzip.compress(pickle.dumps(book_sims) ) ) 

if '--eval' in sys.argv:
  for name in glob.glob('sims/*.json'):
    source = name.split('/').pop().replace('.json', '')
    sims = json.loads(open(name).read() )
    for title, sim in sorted( sims.items(), key=lambda x:x[1]*-1)[:10]:
      print(source, title, sim)
