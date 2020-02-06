from bs4 import BeautifulSoup as soup
import urllib
import requests
import re
import decimal
import logging
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Firestore Config
cred = credentials.Certificate("./uoit-room-finder-ashan.json")

# Initialize Firebase
firebase_admin.initialize_app(cred)

# Get a reference to the database service
db = firestore.client()

prev_crn = 0
epoch = datetime.utcfromtimestamp(0)

class Course(object):
    title = ""
    day = ""
    start_date = ""
    start_time = ""
    end_date = ""
    end_time = ""
    room = ""
    building = ""

    def __init__(self, title, day, start_date, start_time, end_date, end_time, room, building):
        self.title = title
        self.day = day
        self.start_date = start_date
        self.start_time = start_time
        self.end_date = end_date
        self.end_time = end_time
        self.room = room
        self.building = building

# Change the date format to DD/MM/YYYY
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
    elif month == 'Dec':
        month = '12'
    elif month == 'Jan':
        month = '01'
    elif month == 'Feb':
        month = '02'
    elif month == 'Mar':
        month = '03'
    elif month == 'Apr':
        month = '04'
    elif month == 'May':
        month = '05'
    elif month == 'Jun':
        month = '06'
    elif month == 'Jul':
        month = '07'
    else:
        month = '08'

    new_date = year + '-' + month + '-' + day
    return new_date

# Change the time format to 24h
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

def unix_time_seconds(dt):
    return (dt - epoch).total_seconds()

def float_to_string(number, precision=20):
    return u'{0:.{prec}f}'.format(
        decimal.Context(prec=100).create_decimal(str(number)),
        prec=precision,
    ).rstrip('0').rstrip('.') or '0'

def getTimestamp(date, time):
    datetime_str = date + " " + time
    datetime_object = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
    timestamp = unix_time_seconds(datetime_object)
    return float_to_string(timestamp)

def insert_classes(crn, day, start_timestamp, end_timestamp, room, location):
    # When querying SQL DB, only parameters are time and date
    # Checks from nearest hour (round down if before 30, up if after) to the next hour
    #
    #   Course          Start_Date  Start_Time  End_Date    End Time    Room
    #   SOFE2800        Sep 07 2017 9:40AM      Dec 04 2017 11:00AM     UB2080

    map = {
        u'crn': crn,
        u'day': day,
        u'start_timestamp': start_timestamp,
        u'end_timestamp': end_timestamp,
        u'room': room,
        u'location': location
    };

    print(map);

    doc_ref = db.collection(u'classes').document()
    doc_ref.set(map)

def insert_courses (crn, title, subj, code, section, class_type, isLab):

    map = {
        u'crn': crn,
        u'title': title,
        u'subject': subj,
        u'course_code': code,
        u'section': section,
        u'class_type': class_type,
        u'isLab': isLab
    };

    print(map);

    doc_ref = db.collection(u'courses').document()
    doc_ref.set(map)

def createCourse (contents, title, crn, code, subj, section):
    # Lab / Lecture / Tutorial
    class_type = contents[5].get_text()
    isLab = False
    if (class_type == 'Laboratory'):
        isLab = True

    # Time Format => "2:10 pm - 5:00 pm"
    time = contents[1].get_text()
    times = re.split('-', time)

    day = contents[2].get_text()

    if len(times) > 1:
        # Location Format => last string (delimited by spaces) is room #
        location = contents[3].get_text()
        location_array = re.split(' ', location)
        room = location_array[len(location_array) -1]

        building = ' '.join(location_array[:-1])
        fk_building_id = ''
        position = []

        # Assign the FK_BUILDING_ID for the classes
        if(building == 'OPG Engineering Building'):
            fk_building_id = u'OPG'
            position = [
                {
                    u'lat': 43.945772,
                    u'lng': -78.898470
                }
            ]
        elif(building == 'Energy Research Centre (ERC)'):
            fk_building_id = u'ERC'
            position = [
                {
                    u'lat': 43.945668,
                    u'lng': -78.896271
                }
            ]
        elif(building == 'Science Building (UA)'):
            fk_building_id = u'UA'
            position = [
                {
                    u'lat': 43.944509,
                    u'lng': -78.896440
                }
            ]
        elif(building == 'Business and IT Building (UB)'):
           fk_building_id = u'UB'
           position = [
               {
                   u'lat': 43.945162,
                   u'lng': -78.896099
               }
           ]
        elif(building == 'B-Wing'):
            fk_building_id = u'BW'
            position = [
                {
                    u'lat': 43.943585,
                    u'lng': -78.896979
                }
            ]
        elif(building == 'University Pavilion'):
              fk_building_id = u'UP'
              position = [
                  {
                      u'lat': 43.943187,
                      u'lng': -78.898667
                  }
              ]
        elif(building == 'SOUTH WING'):
            fk_building_id = u'SW'
            position = [
                {
                    u'lat': 43.942854,
                    u'lng': -78.896151
                }
            ]
        elif(building == 'Simcoe Building/J-Wing'):
            fk_building_id = u'Simcoe'
            position = [
                {
                    u'lat': 43.945835,
                    u'lng': -78.894623
                },
                {
                    u'lat': 43.945153,
                    u'lng': -78.894744
                },
                {
                    u'lat': 43.944914,
                    u'lng': -78.894626
                }
            ]
        elif(building == 'UL Building'):
            fk_building_id = u'UL'
            position = [
                {
                    u'lat': 43.946217,
                    u'lng': -78.897332
                }
            ]
        elif(building == 'Software and Informatics Resea'):
            fk_building_id = u'SIRC'
            position = [
                {
                    u'lat': 43.947846,
                    u'lng': -78.898861
                }
            ]
        elif(building == 'Bordessa Hall'):
            fk_building_id = u'Bordessa'
            position = [
                {
                    u'lat': 43.898641,
                    u'lng': -78.862043
                }
            ]
        elif(building == 'Regent Theatre'):
            fk_building_id = u'Regent'
            position = [
                {
                    u'lat': 43.898301,
                    u'lng': -78.861992
                }
            ]
        elif(building == 'Education Building'):
            fk_building_id = u'Education'
            position = [
                {
                    u'lat': 43.898021,
                    u'lng': -78.863524
                }
            ]
        elif (building == '61 Charles Street Building'):
            fk_building_id = u'61 Charles'
            position = [
                {
                    u'lat': 43.897385,
                    u'lng': -78.857999
                }
            ]
        else:
            fk_building_id = u'ONLINE'
            position = []

        location = {
            u'building': building,
            u'bid': fk_building_id,
            u'position': position
        }

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

        start_timestamp = getTimestamp(start_date, start_time)
        end_timestamp = getTimestamp(end_date, end_time)

        global prev_crn
        if (prev_crn != crn):
             # Passes values to inert into courses table
            insert_courses(crn, title, subj, code, section, class_type, isLab)

        # Passes values to insert into classes table
        insert_classes(crn, day, start_timestamp, end_timestamp, room, location)

        prev_crn = crn

year = '2020'
# 01 = Winter, 09 = Fall, 05 = Spring/Summer
term = '01'
url = 'https://ssbp.mycampus.ca/prod_uoit/bwckschd.p_get_crse_unsec?term_in='+year+term+'&sel_subj=dummy&sel_subj=&SEL_CRSE=&SEL_TITLE=&BEGIN_HH=0&BEGIN_MI=0&BEGIN_AP=a&SEL_DAY=dummy&SEL_PTRM=dummy&END_HH=0&END_MI=0&END_AP=y&SEL_CAMP=dummy&SEL_SCHD=dummy&SEL_SESS=dummy&SEL_INSTR=dummy&SEL_INSTR=%25&SEL_ATTR=dummy&SEL_ATTR=%25&SEL_LEVL=dummy&SEL_LEVL=%25&SEL_INSM=dummy&sel_dunt_code=&sel_dunt_unit='

r = urllib.urlopen(url)
sauce = soup(r, "lxml")

headers = sauce.find_all('th', {'class' : 'ddheader'})

for header in headers:
    # Get course name
    # Format: Title - CRN - SUBJ_CODE COURSE_CODE - SECTION
    # Special Case: Sp Topics in IT Mgmt - IT Gov - 10904 - MITS 5620G - 001
    title_contents = header.get_text()
    title_contents_array = re.split(' - ', title_contents)

    # To Account for special cases, start from the back
    title = ''
    for x in title_contents_array[:-3]:
        # Title is everything except the last 3 hyphens
        title += x

    # CRN is the 3rd last
    crn = title_contents_array[-3]

    # Course Code is the 2nd last
    code = title_contents_array[-2]

    # Split Course Code into SUBJ and CODE
    codes = re.split(' ', code)
    subj = codes[0]

    # Section # is the last hypen
    section = title_contents_array[-1]

    # Get next row with all the contents
    next_row = header.findNext('tr')

    # Go deeper down into td that contains the content table
    next_td = next_row.findNext('td', {'class' : 'dddefault'})

    # Find all the Border Tables (2)
    border_tables = next_td.find_all('table', {'class' : 'bordertable'})

    # Get the second border table that has all the timing information
    if(len(border_tables)>1):
        contents = border_tables[1].find_all('tr')

    for row in contents:
        #Check if row has dbdefault td's
        if row != contents[0]:
            # Get all the tds (each td contains one piece of info)
            content_tds = row.find_all('td', {'class' : 'dbdefault'})

            # Create a course object for each course
            createCourse(content_tds, title, crn, code, subj, section)
db.close()
