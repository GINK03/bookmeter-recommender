import pickle
import gzip
import json
import sys
import random

if '--count_users' in sys.argv:
  users = set()
  for index, line in enumerate( open('mapped.jsonp') ):
    #print(line)
    line = line.strip()
    if index%1000 == 0:
      print('iter', index)
    try:
      user, obj = line.split('\t')
    except:
      continue
    users.add(user)
  print('total size', len(users))


if '--fold1' in sys.argv:
  key_pair = {}
  for index, line in enumerate( open('mapped.jsonp') ):
    #print(line)
    line = line.strip()
    if index%10000 == 0:
      print('iter', index)
    try:
      key, val = line.split('\t')
    except Exception:
      continue
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
    if ts == []:
      continue
    #print(key, ts)

    labels = []
    for i in range(0, len(ts) - 8):
      start = ts[i]
      #print(start)
      evalDates = [start]
      # 探索する範囲
      for k in range(1, 9):
        es = start.split('/')
        year = int(es[0])
        month = int(es[1])
        if month+k > 12:
          year+=1
          month=month+k-12
        else:
          month=month+k
        nextDate = '{}/{:02d}'.format(year,month)
        #print('gen', nextDate)
        evalDates.append( nextDate )

      label = all( [ edate in ts for edate in evalDates ]  )
      labels.append(label)
    print( json.dumps([1.0 if any(labels) else 0.0 , list(pair['books'])], ensure_ascii=False) )
