import glob

import json

import MeCab

import math

from collections import Counter

import copy

import sys

if '--make' in sys.argv:
  m = MeCab.Tagger('-Owakati') 
  term_freq = {}
  c = 0
  for name in glob.glob('summaries/*.json'):
    c += 1
    obj = json.loads( open(name).read() )
    summary = obj['summary']
    terms = set(m.parse(summary).strip().split())
    for term in terms: 
      if term_freq.get(term) is None:
        term_freq[term] = 0
      term_freq[term] += 1

  idf = {}

  for term, freq in term_freq.items():
    idf[term] = math.log(c/freq)

  for name in glob.glob('summaries/*.json'):
    obj = json.loads( open(name).read() )
    title = obj['title']
    summary = obj['summary']
    term_freq = dict( Counter(m.parse(summary).strip().split()) )

    term_score = {}
    for term, freq in term_freq.items():
      term_score[term] = freq * idf[term] 
    
    save_name = name.split('/').pop()
    open('tfidf/{}'.format(save_name), 'w').write( json.dumps(term_score, indent=2, ensure_ascii=False) )

if '--similarity' in sys.argv:
  book_tfidf = {}
  for name in glob.glob('tfidf/*.json'):
    obj = json.loads( open(name).read() )
    book = name.split('/').pop().replace('.json', '')
    book_tfidf[book] = obj 

  book_tfidf_ = copy.copy(book_tfidf)
  for book, tfidf in book_tfidf_.items():
    book_score = {}
    for _book, _tfidf in book_tfidf.items():
      dot = sum( [f*_tfidf[t] for t,f in tfidf.items() if _tfidf.get(t) is not None] )
      norm = (sum([v**2 for v in tfidf.values()]) * sum([v**2 for v in _tfidf.values()]) )**0.5
      book_score[_book] = dot/norm
    print(book) 
    book_score = { book:score for book, score in sorted( book_score.items(), key=lambda x:x[1]*-1)[:10] }
    print( json.dumps(book_score, indent=2, ensure_ascii=False) )
