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

    def __init__(title, day, start_date, start_time, end_date, end_time, room, building):
        self.title = title
        self.day = day
        self.start_date = start_date
        self.start_time = start_time
        self.end_date = end_date
        self.end_time = end_time
        self.room = room
        self.building = building

def changeDateFormat(date):
    # Current Format => Sep 07 2017
    # New Format => 07/09/2017
    date_array = re.split(' ', date)
    day = date_array[1]
    month = date_array[0]
    year = date_array[2]
    if month == 'Sep':
        month = '09'
    elif month == 'Oct':
        month = '10'
    elif month == 'Nov':
        month = '11'
    else:
        month = '12'

    new_date = year + '-' + month + '-' + day
    return new_date

def changeTimeFormat(time):
    # Current Format => 1:10 pm
    # New Format => 13:10
    newTime = ''
    time = time.strip()
    time_array = re.split(' ', time)
    if time_array[1] == 'pm':
        times = re.split(':', time_array[0])
        num = int(times[0])
        if(num == 12):
            newTime = time_array[0]
        else:
            num = num + 12
        newTime = str(num) + ':' + times[1]
    elif time_array[1] == 'am':
        newTime = time_array[0]
    return newTime

def db_insert(title, day, start_date, start_time, end_date, end_time, room, building):
    # When querying SQL DB, only parameters are time and date
    # Checks from nearest hour (round down if before 30, up if after) to the next hour
    #
    #   Course          Start_Date  Start_Time  End_Date    End Time    Room
    #   SOFE2800        Sep 07 2017 9:40AM      Dec 04 2017 11:00AM     UB2080

    # Open database connection
    db = MySQLdb.connect("localhost", "root", "testpass", "Room Finder" )

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    values = "('" + title + "','" + day + "','" + start_date + "','" + start_time
    values += "','" + end_date + "','" + end_time + "','" + room + "','" + building  + "'),"
    # values = "('" + room + "'),"
    print (values)

def createCourse (contents, title):

    # Time Format => "2:10 pm - 5:00 pm"
    time = contents[1].get_text()
    times = re.split('-', time)

    day = contents[2].get_text()

    if len(times) > 1:
        # Location Format => last string (delimited by spaces) is room #
        location = contents[3].get_text()
        location_array = re.split(' ', location);
        room = location_array[len(location_array) -1]

        building = ' '.join(location_array[:-1]);

        # Date Range Format => "Sep 07, 2017 - Dec 04, 2017"
        date_range = contents[4].get_text()
        date_array = re.split(', | - ', date_range)

        start_date = date_array[0] + ' ' + date_array[1]
        start_date = changeDateFormat(start_date)

        start_time = times[0]
        start_time = changeTimeFormat(start_time)

        end_date = date_array[2] + ' ' + date_array[3]
        end_date = changeDateFormat(end_date)

        end_time = times[1]
        end_time = changeTimeFormat(end_time)

        db_insert(title, day, start_date, start_time, end_date, end_time, room, building)

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
