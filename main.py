import bs4 as bs
import requests


url = raw_input("enter a website url")

sauce = urllib2.urlopen(url);

soup = bs.BeautifulSoup(sauce, 'lxml');

print(soup);
