import plyvel

import os

import sys

db = plyvel.DB('htmls.ldb')
for key,val in db:
  key = key.decode('utf8')
  if 'users' in key:
    print(key)
