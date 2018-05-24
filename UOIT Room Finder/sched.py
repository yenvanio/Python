from bs4 import BeautifulSoup as soup
import urllib
import requests
import re
import logging
import MySQLdb

prev_crn = 0
db = MySQLdb.connect(host="localhost",  # your host, usually localhost
                    user="root",        # your username
                    passwd="testpass",  # your password
                    db="Room Finder")   # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()

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

def insert_classes(crn, day, start_date, start_time, end_date, end_time, room, fk_building_id):
    # When querying SQL DB, only parameters are time and date
    # Checks from nearest hour (round down if before 30, up if after) to the next hour
    #
    #   Course          Start_Date  Start_Time  End_Date    End Time    Room
    #   SOFE2800        Sep 07 2017 9:40AM      Dec 04 2017 11:00AM     UB2080

    sql = "INSERT INTO class (fk_course_crn, day, start_date, start_time, end_date, end_time, room, fk_building_id) VALUES "
    sql += "(" + crn + ",'" + day + "','" + start_date + "','" + start_time
    sql += "','" + end_date + "','" + end_time + "','" + room + "','" + fk_building_id  + "')"
    print (sql)

    global db, cur 
    cur.execute(sql)
    db.commit()

def insert_courses (crn, title, subj, code, section, class_type):

    sql = "INSERT INTO course (crn, title, subject, code, section, type) VALUES " 
    sql += "(" +crn + ",'" + title + "','" + subj + "','" + code
    sql += "'," + section + ",'" + class_type + "')"
    print (sql)
    
    global db, cur 
    cur.execute(sql)
    db.commit()

def createCourse (contents, title, crn, code, subj, section):
    # Lab / Lecture / Tutorial
    class_type = contents[5].get_text()

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

        if(building == 'OPG Engineering Building'):
            fk_building_id = 'OPG'
        elif(building == 'Energy Research Centre (ERC)'):
            fk_building_id = 'ERC'
        elif(building == 'Science Building (UA)'):
            fk_building_id = 'UA'
        elif(building == 'Business and IT Building (UB)'):
            fk_building_id = 'UB'
        elif(building == 'B-Wing'):
            fk_building_id = 'BW'
        elif(building == 'University Pavilion'):
            fk_building_id = 'UP'
        elif(building == 'SOUTH WING'):
            fk_building_id = 'SW'
        elif(building == 'Simcoe Building/J-Wing'):
            fk_building_id = 'Simcoe'
        elif(building == 'UL Building'):
            fk_building_id = 'UL'
        elif(building == 'Software and Informatics Resea'):
            fk_building_id = 'SIRC'
        elif(building == 'Bordessa Hall'):
            fk_building_id = 'Bordessa'
        elif(building == 'Regent Theatre'):
            fk_building_id = 'Regent'
        elif(building == 'Education Building'):
            fk_building_id = 'Education'
        elif (building == '61 Charles Street Building'):
            fk_building_id = '61 Charles'
        elif (building == 'University Building A1'):
            fk_building_id = 'UA'
        elif(building == 'Virtual Adobe Connect'):
            fk_building_id = 'ONLINE'


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

        global prev_crn
        if (prev_crn != crn):
            # Passes values to inert into courses table 
            insert_courses(crn, title, subj, code, section, class_type)
        
        # Passes values to insert into classes table
        insert_classes(crn, day, start_date, start_time, end_date, end_time, room, fk_building_id)

        prev_crn = crn

year = '2018'
# 01 = Winter, 09 = Fall, 05 = Spring/Summer
term = '05'
url = 'https://ssbp.mycampus.ca/prod_uoit/bwckschd.p_get_crse_unsec?TRM=U&term_in='+year+term+'&sel_subj=dummy&sel_day=dummy&sel_schd=dummy&sel_insm=dummy&sel_camp=dummy&sel_levl=dummy&sel_sess=dummy&sel_instr=dummy&sel_ptrm=dummy&sel_attr=dummy&sel_subj=&sel_crse=&sel_title=&sel_schd=&sel_insm=%25&sel_from_cred=&sel_to_cred=&sel_camp=%25&begin_hh=0&begin_mi=0&begin_ap=p&end_hh=0&end_mi=0&end_ap=a'

r = urllib.urlopen(url)
sauce = soup(r, "lxml")

headers = sauce.find_all('th', {'class' : 'ddheader'})

for header in headers:
    # Get course name
    # Format: Title - CRN - SUBJ_CODE COURSE_CODE - SECTION
    # Special Case: Sp Topics in IT Mgmt - IT Gov - 10904 - MITS 5620G - 001
    title_contents = header.get_text()
    title_contents_array = re.split(' - ', title_contents)

    title = ''
    for x in title_contents_array[:-3]:
        title += x

    crn = title_contents_array[-3]
    
    code = title_contents_array[-2]
    codes = re.split(' ', code)

    subj = codes[0]

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