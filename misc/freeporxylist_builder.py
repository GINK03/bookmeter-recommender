import requests


import bs4

url = 'https://free-proxy-list.net/'
r = requests.get(url, proxies={'https': '211.127.160.240:8080'} )
print( r.text )

soup = bs4.BeautifulSoup( r.text )

import json

proxies = []
for tr in soup.find_all('tr'):
  tds =  tr.find_all('td')
  if len(tds) <= 3:
    continue
  ip = tds[0].text
  port = tds[1].text
  code = tds[2].text
  print(ip, port, code)
  proxies.append( (ip, port, code) )

open('proxies.json', 'w').write( json.dumps(proxies, indent=2) )
