import json
import sys


if '--normal' in sys.argv:
  book_freq = {}
  for index, line in enumerate(open('dump.jsonp')):
    if index%1000 == 0:
      print('iter', index, file=sys.stderr )
    line = line.strip()
    flag, books = json.loads( line )
    for book in books:
      if book_freq.get(book) is None:
        book_freq[book] = 0
      book_freq[book] += 1

  for book, freq in sorted(book_freq.items(), key=lambda x:x[1]*-1):
    print( book, freq )

if '--6month' in sys.argv:
  book_freq_0 = {}
  book_freq_1 = {}
  for index, line in enumerate(open('dump.jsonp')):
    if index%1000 == 0:
      print('iter', index, file=sys.stderr )
    line = line.strip()
    flag, books = json.loads( line )
    for book in books:
      if flag == 1:
        if book_freq_1.get(book) is None:
          book_freq_1[book] = 0
        book_freq_1[book] += 1
      if flag == 0:
        if book_freq_0.get(book) is None:
          book_freq_0[book] = 0
        book_freq_0[book] += 1

  for book, freq in sorted(book_freq_0.items(), key=lambda x:x[1]*-1):
    print('0', book, freq )
