
import json

import os

import sys


time_pages = {}
for line in open('mapped.jsonp'):
  line = line.strip()
  try:
    user,  val = line.split('\t')
  except ValueError:
    continue
  val = json.loads(val)
  page = val['page']
  date = val['date']
  try:
    year,month, day = date.split('/')
  except ValueError:
    continue
  time = '{}/{}'.format(year,month)
  if time_pages.get(time) is None:
    time_pages[time] = 0
  time_pages[time] += int(page)
  #print( page, date )

for time, pages in sorted(time_pages.items(), key=lambda x:x[0]):
  print(time, pages)
