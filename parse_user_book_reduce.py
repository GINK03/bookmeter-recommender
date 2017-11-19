import pickle
import gzip
import json
import sys

if '--fold1' in sys.argv:
  key_pair = {}
  for line in open('mapped.jsonp'):
    line = line.strip()
    key, val = line.split('\t')
    if key_pair.get(key) is None:
      key_pair[key] = {'time-series':set(), 'books':set()}

    val = json.loads(val)
    title = val['title'].strip().replace(' ', '')
    dates = val['date'].split('/')
    try:
      date = '{}/{}'.format(dates[0], dates[1])
    except IndexError as e:
      continue
    key_pair[key]['time-series'].add( date )
    key_pair[key]['books'].add( title )

  open('tmp/key_pair.pkl.gz', 'wb').write( gzip.compress( pickle.dumps( key_pair ) ) )

if '--label1' in sys.argv:
  key_pair = pickle.loads( gzip.decompress( open('tmp/key_pair.pkl.gz', 'rb').read() ) )
 
  for key, pair in key_pair.items():
    ts = sorted( pair['time-series'] )
    print(key, ts)

    labels = []
    for i in range(0, len(ts) - 2):
      start = ts[i]
      print(start)
      evalDates = [start]
      # 探索する範囲
      for k in range(1, 3):
        es = start.split('/')
        year = int(es[0])
        month = int(es[1])
        if month+k > 12:
          year+=1
          month=month+k-12
        else:
          month=month+k
        nextDate = '{}/{:02d}'.format(year,month)
        print('gen', nextDate)
        evalDates.append( nextDate )

      label = all( [ edate in ts for edate in evalDates ]  )
      labels.append(label)
    print(labels, pair['books'] )
