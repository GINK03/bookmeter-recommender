import json

f = open('dataset.txt', 'w')
for line in open('dump.jsonp'):
  line = line.strip()
  #print( line )
  flag, books = json.loads(line)
  books = [book.replace(' ', '').replace('　', '') for book in books] 
  f.write( ' '.join( books ) + '\n' )
