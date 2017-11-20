import json
import os
import sys

if '--map1' in sys.argv:
  booksset = set()
  for line in open('dump.jsonp'):
    line = line.strip()
    ans, books = json.loads( line )
    for book in books:
      booksset.add(book)

  book_index = {}
  for index, book in enumerate(list(booksset)):
    book_index[book] = index

  open('book_index.json', 'w').write( json.dumps(book_index, indent=2, ensure_ascii=False) )

if '--map2' in sys.argv:
  
  book_index = json.loads( open('book_index.json').read() )

  for line in open('dump.jsonp'):
    line = line.strip()
    ans, books = json.loads( line )
    
    sparse = ' '.join(['{}:1.0'.format(book_index[book]) for book in books] )
    print('{} {}'.format(ans, sparse))
