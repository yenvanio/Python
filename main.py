import urllib3
http = urllib3.PoolManager()
response = http.request('GET', 'http://www.crummy.com/software/BeautifulSoup/')

from bs4 import BeautifulSoup
soup = BeautifulSoup(response.data)
