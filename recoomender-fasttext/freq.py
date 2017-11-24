import json
import sys
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
