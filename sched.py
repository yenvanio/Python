from bs4 import BeautifulSoup as soup
import urllib
from lxml import html
import requests
import json

def createCourse (contents, title):
        week = contents[0].get_text()
        time = contents[1].get_text()
        day = contents[2].get_text()
        location = contents[3].get_text()
        date_range = contents[4].get_text()
        type_of = contents[5].get_text()
        print(week+time+day+location+date_range+type_of)


class Course(object):
    title = ""
    week = ""
    time = ""
    day = ""
    location = ""
    date_range = ""
    type_of = ""

    def __init__(title, week, time, day, location, date_range, type_of):
        self.title = title
        self.week = week
        self.time = time
        self.day = day
        self.location = location
        self.date_range = date_range
        self.type_of = type_of

url = 'https://ssbp.mycampus.ca/prod_uoit/bwckschd.p_get_crse_unsec?TRM=U&term_in=201709&sel_subj=dummy&sel_day=dummy&sel_schd=dummy&sel_insm=dummy&sel_camp=dummy&sel_levl=dummy&sel_sess=dummy&sel_instr=dummy&sel_ptrm=dummy&sel_attr=dummy&sel_subj=&sel_crse=&sel_title=&sel_schd=&sel_insm=%25&sel_from_cred=&sel_to_cred=&sel_camp=%25&begin_hh=0&begin_mi=0&begin_ap=p&end_hh=0&end_mi=0&end_ap=a'

r = urllib.urlopen(url)
sauce = soup(r, "lxml")

headers = sauce.find_all('th', {'class' : 'ddheader'})

for header in headers:
    title = header.get_text()
    print(title)
    next_row = header.findNext('tr')
    next_td = next_row.findNext('td', {'class' : 'dddefault'})
    border_table = next_td.find_all('table', {'class' : 'bordertable'})
    contents = border_table[1].find_all('td', {'class' : 'dbdefault'})
    createCourse(contents, title)
