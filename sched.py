from bs4 import BeautifulSoup as soup
import urllib
import requests
import re
import MySQLdb
import logging

class Course(object):
    title = ""
    start_date = ""
    end_date = ""
    room = ""

    def __init__(title, start_date, end_date, room):
        self.title = title
        self.start_date = start_date
        self.end_date = end_date
        self.room = room

def db_insert(title, start_date, end_date, room):
    # When querying SQL DB, only parameters are time and date
    # Checks from nearest hour (round down if before 30, up if after) to the next hour
    #
    #   Course          Start_Date              End_Date                Room
    #   SOFE2800        Sep 07 2017 9:40am      Dec 04 2017 11:00am     UB2080

    # Open database connection
    db = MySQLdb.connect("localhost", "root", "testpass", "Room Finder" )

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    values = "('" + title + "','" + start_date + "','" + end_date + "','" + room + "'),"
    print (values)

def createCourse (contents, title):

    # Time Format => "2:10 - 5:00"
    time = contents[1].get_text()
    times = re.split('-', time)

    if len(times) > 1:
        # Location Format => last string (delimited by spaces) is room #
        location = contents[3].get_text()
        room = re.split(' ', location)[-1:]

        # Date Range Format => "Sep 07, 2017 - Dec 04, 2017"
        date_range = contents[4].get_text()
        date_array = re.split(', | - ', date_range)

        start_date = date_array[0] + ' ' + date_array[1] + ' ' + times[0]
        end_date = date_array[2] + ' ' + date_array[3] + ' ' + times[1]

        db_insert(title, start_date, end_date, room[0])

url = 'https://ssbp.mycampus.ca/prod_uoit/bwckschd.p_get_crse_unsec?TRM=U&term_in=201709&sel_subj=dummy&sel_day=dummy&sel_schd=dummy&sel_insm=dummy&sel_camp=dummy&sel_levl=dummy&sel_sess=dummy&sel_instr=dummy&sel_ptrm=dummy&sel_attr=dummy&sel_subj=&sel_crse=&sel_title=&sel_schd=&sel_insm=%25&sel_from_cred=&sel_to_cred=&sel_camp=%25&begin_hh=0&begin_mi=0&begin_ap=p&end_hh=0&end_mi=0&end_ap=a'

r = urllib.urlopen(url)
sauce = soup(r, "lxml")

headers = sauce.find_all('th', {'class' : 'ddheader'})

for header in headers:
    # Get course name
    title = header.get_text()

    # Get next row with all the contents
    next_row = header.findNext('tr')

    # Go deeper down into td that contains the content table
    next_td = next_row.findNext('td', {'class' : 'dddefault'})

    # Find all the Border Tables (2)
    border_tables = next_td.find_all('table', {'class' : 'bordertable'})

    # Get the second border table that has all the timing information
    contents = border_tables[1].find_all('tr')

    for row in contents:
        #Check if row has dbdefault td's
        if row != contents[0]:
            # Get all the tds (each td contains one piece of info)
            content_tds = row.find_all('td', {'class' : 'dbdefault'})

            # Create a course object for each course
            createCourse(content_tds, title)
